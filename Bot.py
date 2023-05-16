import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode, AllowedUpdates

from src.config import Config

import betterlogging as bl

from src import middlewares, handlers

from src.database.services.db_engine import create_db_engine_and_session_pool

log = logging.getLogger(__name__)


async def main():
    config = Config.from_env()
    bl.basic_colorized_config(level=config.misc.log_level)
    log.info('Start')

    storage = RedisStorage2(host=config.redis.host, port=config.redis.port)

    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)

    db_engine, sqlalchemy_session_pool = await create_db_engine_and_session_pool(config.db.sqlalchemy_url)
    middlewares.setup(dp, sqlalchemy_session_pool)

    handlers.setup(dp)

    allowed_updates = (AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY)

    try:
        await dp.skip_updates()
        await dp.start_polling(allowed_updates=allowed_updates, )
    finally:
        await storage.close()
        await storage.wait_closed()
        await (await bot.get_session()).close()
        await db_engine.dispose()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        log.warning('Бот зупинено')
