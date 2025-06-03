import os

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from config import Settings
from src.dialogs.bot_menu.states import BotMenu
from src.lexicon.lexicon_ru import MAIN_MENU, LEXICON_RU

from src.services.repo import Repo, Rent

settings = Settings()

src_dir = os.path.normpath(os.path.join(os.getcwd(),settings.PATH_IMG))

async def get_main_menu(dialog_manager: DialogManager, **middleware_data):
    return {'main_menu': MAIN_MENU}

async def get_categories(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session_with_commit')
    data = await Repo.get_all_categories(session)
    return {'categories':data}

async def get_rents(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session_with_commit')
    ctx = dialog_manager.current_context()
    category_id = ctx.dialog_data.get('category_id')

    if not category_id:
        await dialog_manager.event.answer(LEXICON_RU['error_category'])
        await dialog_manager.switch_to(BotMenu.select_categories)
        return

    data = await Repo.get_rents_by_category(session=session, category_id=category_id)
    return {'rents':data}


async def get_rent_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session_with_commit')
    ctx = dialog_manager.current_context()
    rent_id = ctx.dialog_data.get('rent_id')

    rent:Rent = await Repo.get_rent_by_id(rent_id = rent_id, session=session)
    ctx.dialog_data.update(price_id=rent.price_id)
    photo = MediaAttachment(type=ContentType.PHOTO, path=os.path.join(src_dir, rent.img + '.png'))

    return {'rent_info':rent,'photo':photo}


async def get_price_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session_with_commit')
    ctx = dialog_manager.current_context()
    price_id = ctx.dialog_data.get('price_id')

    price_info = await Repo.get_price_info_by_id(price_id=price_id, session=session)

    return {'price_info':price_info}


async def get_order_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session_with_commit')
    ctx = dialog_manager.current_context()
    rent_id:int = ctx.start_data.get('rent_id')
    period_id:int = ctx.start_data.get('period_id')

    print(f'rent_id: {rent_id}, period_id: {period_id}')

    order_info = await Repo.get_order_info(
        rent_id=rent_id,
        period_id=period_id,
        session=session
    )

    return {'order_info':order_info}