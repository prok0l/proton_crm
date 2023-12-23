from aiogram import types, Dispatcher

from crmproton.management.commands.tg_bot.services.db_api import check_user,\
    create_user
from ..services.consts import Start


async def bot_start(message: types.Message):
    from_user = int(message.chat.id)
    is_in_db = await check_user(tg_id=from_user)
    if not is_in_db:
        await create_user(tg_id=from_user)

    await message.answer(Start.START.value.format(from_user=from_user))


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=["start"])
