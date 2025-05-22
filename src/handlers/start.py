from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, DialogManager, StartMode

from src.dialogs import register_dialogs
from src.dialogs.bot_menu.states import BotMenu

router: Router = Router()
register_dialogs(router)

@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotMenu.main_menu, mode=StartMode.RESET_STACK)