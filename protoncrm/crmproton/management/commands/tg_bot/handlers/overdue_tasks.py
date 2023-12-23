import asyncio
import aioschedule
from typing import List, Literal

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from crmproton.models import Tasks
from ..services.consts import Overdue
from ..services.db_api import tasktime_overduelist, get_info_about_overdue,\
    tasktime_reminded
from django.conf import settings


host = settings.ALLOWED_HOSTS
host = host[1] if host else 'http://127.0.0.1:8080'


bot: Bot
remind_time: int


async def search_overdue():
    links = await tasktime_overduelist()
    for link in links:
        users = await get_info_about_overdue(link)
        await send_alerts(task=link.task, users=users,
                          text=Overdue.OVERDUE)


async def search_reminded():
    global remind_time
    links = await tasktime_reminded(remind_time)
    for link in links:
        users = await get_info_about_overdue(link, is_overdue=False)
        await send_alerts(task=link.task, users=users,
                          text=Overdue.SOON)


async def send_alerts(task: Tasks, users: List[int],
                      text: Literal[Overdue.OVERDUE,
                                    Overdue.SOON]):
    global bot
    for user in users:
        await asyncio.sleep(0.1)
        task_id = task.__getattribute__("id")
        await bot.send_message(chat_id=user,
                               text=text.value.format(id=task_id, host=host))


async def overdue_tasks(dp: Dispatcher, rmd_time: int):
    global bot, remind_time
    bot = dp.bot
    remind_time = rmd_time
    aioschedule.every(1).minutes.do(search_reminded)
    aioschedule.every(1).minutes.do(search_overdue)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
