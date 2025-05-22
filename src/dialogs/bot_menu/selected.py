from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.dialogs.bot_menu.states import BotMenu


async def on_chosen_category(
        c: CallbackQuery,
        widget:Select,
        manager:DialogManager,
        item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(category_id=item_id)
    await manager.switch_to(BotMenu.select_products)