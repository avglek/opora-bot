from aiogram_dialog import DialogManager

from src.lexicon.lexicon_ru import MAIN_MENU


async def get_categories(dialog_manager: DialogManager, **middleware_data):
    # session = middleware_data.get('session')
    # repo:Repo = middleware_data.get('repo')
    # db_categories = await repo.get_categories(session)
    #
    # data = {
    #     'categories': [
    #         (f'{category.name} ({len(category.items)})', category.category_id)
    #         for category in db_categories
    #     ]
    # }

    data = {
            'categories': [
                ('Категория 1', 1),
                ('Категория 2', 2),
                ('Категория 3', 3),
            ]
    }

    return data

async def get_main_menu(dialog_manager: DialogManager, **middleware_data):
    data = {
        'main_menu': MAIN_MENU
    }
    return data