import asyncio
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config import Settings
from src.handlers import start, echo
from src.middleware.database_middleware import DatabaseMiddlewareWithoutCommit, DatabaseMiddlewareWithCommit

# Функция, которая выполнится когда бот запустится
async def start_bot():
    logger.info("Бот успешно запущен.")


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    logger.info("Бот остановлен!")

async def main():

    settings = Settings()

    # Инициализируем бота и диспетчер
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    #admins = settings.ADMIN_IDS

    #log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
    #logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)
    logger.add(sys.stdout,format=settings.FORMAT_LOG, level="INFO")

    # регистрация мидлварей
    dp.update.middleware.register(DatabaseMiddlewareWithoutCommit())
    dp.update.middleware.register(DatabaseMiddlewareWithCommit())

    # регистрация роутеров
    #dp.include_router(start.router)
    dp.include_router(start.router)

    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
