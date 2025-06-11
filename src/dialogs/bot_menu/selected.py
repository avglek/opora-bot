from typing import Any

from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from src.dialogs.bot_menu.states import BotMenu, MessageGroup, OrderRent
from src.models.repo_model import User, Order
from src.services.repo import Repo


async def on_chosen_menu(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(hello_id=item_id)
    if item_id =='1':
        await manager.switch_to(BotMenu.select_categories)
    elif item_id == '2':
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


async def on_chosen_price(c: CallbackQuery, widget:Select, manager:DialogManager):
    await manager.switch_to(BotMenu.price_info)


async def on_chosen_home(c: CallbackQuery, widget:Select, manager:DialogManager):
    await manager.switch_to(BotMenu.main_menu)


async def on_chosen_price_info(c: CallbackQuery, widget:Select, manager:DialogManager, item_id:str):
    ctx = manager.current_context()
    ctx.dialog_data.update(period_id=item_id)
    await manager.start(OrderRent.add_to_order,data=ctx.dialog_data)


async def on_chosen_add_to_order(m:Message, widget:Select, manager:DialogManager,quantity:str):
    ctx = manager.current_context()
    user:User = User(
        telegram_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        name=m.from_user.username
    )
    order:Order = Order(
        rent_id=ctx.start_data['rent_id'],
        period_id=ctx.start_data['period_id'],
        quantity=int(quantity),
    )
    ctx.dialog_data.update(
        order = order,
        user = user
    )
    await manager.switch_to(OrderRent.order_info)

async def send_contact(cq: CallbackQuery, _, dialog_manager: DialogManager):
    markup = ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="Поделиться контактом", request_contact=True)
    ]], resize_keyboard=True)
    message = await cq.message.answer("Нажмите на кнопку ниже:", reply_markup=markup)
    dialog_manager.dialog_data["message_id"] = message.message_id