from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.dialogs.bot_menu.states import BotMenu, MessageGroup

async def on_chosen_menu(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(hello_id=item_id)
    if item_id in ('1', '2'):
        await manager.switch_to(BotMenu.select_categories)
    elif item_id == '3':
        await manager.start(MessageGroup.add_contact)
    else:
        await manager.start(MessageGroup.add_contact)

async def on_chosen_add_contact(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    print('add contact')

async def on_chosen_category(c: CallbackQuery,widget:Select,manager:DialogManager,item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenu.select_rents)

async def on_chosen_rents(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(rent_id=item_id)
    await manager.switch_to(BotMenu.rent_info)