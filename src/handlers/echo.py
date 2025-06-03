from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router: Router = Router()

@router.message(Command('start'))
async def start(message: Message):
    await message.reply('Привет, я эхо бот:')