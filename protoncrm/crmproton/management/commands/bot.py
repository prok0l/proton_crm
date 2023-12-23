import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from asgiref.sync import async_to_sync
from django.core.management import BaseCommand

from .tg_bot.config import load_config, BotConfig
from .tg_bot.handlers.start import register_start
from .tg_bot.handlers.overdue_tasks import overdue_tasks


async def register_all_handlers(dp: Dispatcher, config: BotConfig):
    tasks = [asyncio.create_task(start_bot(dp)),
             asyncio.create_task(overdue_tasks(dp,
                                               rmd_time=config.remind_time)),
             ]
    register_start(dp)
    await asyncio.gather(*tasks)


async def start_bot(dp: Dispatcher):
    bot = dp.bot
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.wait_closed()
        session = await bot.get_session()
        await session.close()


async def main():
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d '
                               u'#%(levelname)-8s'
                               u' [%(asctime)s] - %(name)s'
                               u' - %(message)s')
    config: BotConfig = load_config()
    bot = Bot(token=config.token, parse_mode="HTML")
    storage = RedisStorage2() if config.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    await register_all_handlers(dp, config)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        try:
            asyncio.run(main=main())
        except (KeyboardInterrupt, SystemExit):
            logger.error("BOT STOPPED!!!")

