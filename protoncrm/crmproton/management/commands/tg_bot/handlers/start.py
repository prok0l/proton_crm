from aiogram import types, Dispatcher

from crmproton.management.commands.tg_bot.services.db_api import (check_user,
                                                                  create_user,
                                                                  deeplink)
from ..services.consts import Start


async def bot_start(message: types.Message):
    username = message.get_args()
    tg_id = int(message.chat.id)
    is_in_db = await check_user(tg_id)
    if not is_in_db:
        await create_user(tg_id)
    if username and await deeplink(username, tg_id):
        await message.answer(Start.DEEPLINK.value)
    else:
        await message.answer(Start.START.value.format(from_user=tg_id))


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=["start"])
