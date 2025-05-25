import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import Config, load_config
from src.handlers import start
from src.middleware.custom_middleware import CustomMiddleware
from src.services.repo import Repo

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting bot')

    config: Config = load_config()

    engine = create_engine(config.db.get_local_url(), echo=True)
    session = Session(engine)
    repo = Repo(session)

    bot: Bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp: Dispatcher = Dispatcher()

    dp.update.middleware(CustomMiddleware(repo))
    dp.include_router(start.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
