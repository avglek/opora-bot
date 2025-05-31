import os

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from config import Config, load_config
from src.dialogs.bot_menu.states import BotMenu
from src.lexicon.lexicon_ru import MAIN_MENU, LEXICON_RU

from src.services.repo import Repo, Rent

config:Config = load_config()

src_dir = os.path.normpath(os.path.join(os.getcwd(),config.path_img))

async def get_main_menu(dialog_manager: DialogManager, **middleware_data):
    return {'main_menu': MAIN_MENU}

async def get_categories(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')
    data = await repo.get_all_categories()
    return {'categories':data}

async def get_rents(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')

    ctx = dialog_manager.current_context()
    category_id = ctx.dialog_data.get('category_id')
    if not category_id:
        await dialog_manager.event.answer(LEXICON_RU['error_category'])
        await dialog_manager.switch_to(BotMenu.select_categories)
        return

    data = await repo.get_rents_by_category(category_id)
    return {'rents':data}


async def get_rent_info(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')

    ctx = dialog_manager.current_context()
    rent_id = ctx.dialog_data.get('rent_id')

    rent:Rent = await repo.get_rent_by_id(rent_id)
    ctx.dialog_data.update(price_id=rent.price_id)
    photo = MediaAttachment(type=ContentType.PHOTO, path=os.path.join(src_dir, rent.img + '.png'))

    return {'rent_info':rent,'photo':photo}


async def get_price_info(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()

    price_id = ctx.dialog_data.get('price_id')
    price_info = await repo.get_price_info_by_id(price_id)

    return {'price_info':price_info}


async def get_order_info(dialog_manager: DialogManager, **middleware_data):
    repo:Repo = middleware_data.get('repo')
    ctx = dialog_manager.current_context()
    print(ctx.start_data)
    rent_id = ctx.start_data.get('rent_id')
    price_id = ctx.start_data.get('price_id')
    period_id = ctx.start_data.get('period_id')

    order_info = await repo.get_order_info(
        rent_id=rent_id,
        price_id=price_id,
        period_id=period_id
    )

    return {'order_info':order_info}