from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, DialogManager, StartMode

from .dialog import dialog, DialogSG

router: Router = Router()

router.include_router(dialog)
setup_dialogs(router)

@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DialogSG.home, mode=StartMode.RESET_STACK)