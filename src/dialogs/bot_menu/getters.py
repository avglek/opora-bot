from aiogram_dialog import DialogManager

from src.lexicon.lexicon_ru import MAIN_MENU
from src.services.repo import Repo


async def get_categories(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')
    data = repo.get_categories()
    return data

async def get_main_menu(dialog_manager: DialogManager, **middleware_data):
    data = {
        'main_menu': MAIN_MENU
    }
    return data