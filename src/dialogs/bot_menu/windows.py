from typing import Any

from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Back, Next, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, List
from src.dialogs.bot_menu import selected, states, getters, keyboards
from src.dialogs.bot_menu.states import BotMenu
from src.lexicon.lexicon_ru import LEXICON_RU, CONST_BACK, CONST_CATEGORY


def main_menu_window() -> Window:
    return Window(
        Const(LEXICON_RU['/start']),
        keyboards.main_menu_keyboard(selected.on_chosen_menu),
        Cancel(Const('Exit')),
        state=states.BotMenu.main_menu,
        getter=getters.get_main_menu
    )

def categories_window()-> Window:
    return Window(
        Const(LEXICON_RU['/categories']),
        keyboards.paginated_categories(selected.on_chosen_category),
        Back(Const(CONST_BACK)),
        keyboards.home_button(selected.on_chosen_home),
        state=states.BotMenu.select_categories,
        getter=getters.get_categories
    )

def rents_window() -> Window:
    return Window(
        Const(LEXICON_RU['/rents']),
        keyboards.rents_keyboard(selected.on_chosen_rents),
        Back(Const(CONST_BACK)),
        keyboards.home_button(selected.on_chosen_home),
        state=states.BotMenu.select_rents,
        getter=getters.get_rents
    )

def rent_info_window() -> Window:
    return Window(
        Format('{rent_info.name}'),
        Format('{rent_info.description}'),
        DynamicMedia(selector='photo'),
        keyboards.rent_info_keyboard(selected.on_chosen_price),
        Back(Const(CONST_BACK)),
        keyboards.home_button(selected.on_chosen_home),
        state=states.BotMenu.rent_info,
        getter=getters.get_rent_info
    )

def price_info_window()-> Window:
    return Window(
        Const(LEXICON_RU['/price_info']),
        keyboards.price_info_keyboard(selected.on_chosen_price_info),
        Back(Const(CONST_BACK)),
        keyboards.home_button(selected.on_chosen_home),
        state=states.BotMenu.price_info,
        getter=getters.get_price_info
    )

def order_rent_window()-> Window:
    return Window(
        Const(LEXICON_RU['/order_rent']),
        Back(Const(CONST_BACK)),
        state=states.BotMenu.order_rent
    )

def add_contact_window()-> Window:
    return Window(
        Const(LEXICON_RU['/continue']),
        MessageInput(selected.get_contact, ContentType.CONTACT),
        state=states.MessageGroup.add_contact
    )

def send_contact_window()-> Window:
    return Window(
        Const(LEXICON_RU['/info_contact']),
        Next(Const(LEXICON_RU['/send_contact']),on_click = selected.send_contact),
        Cancel(Const('Exit')),
        state=states.MessageGroup.send_contact
    )

def add_to_order_window()-> Window:
    return Window(
        Format('Вы выбрали:{order_info.rent_name}\nСрок аренды: {order_info.period_ru}\nЦена: {order_info.price} ({order_info.currency})'),
        Const('Введите количество:'),
        TextInput(
            id='quantity',
            on_error=error,
            on_success=selected.on_chosen_add_to_order,
            type_factory=int,
        ),
        Cancel(
            Const(CONST_BACK)
        ),
        getter=getters.get_order_info,
        state=states.OrderRent.add_to_order
    )

def order_window()-> Window:
    return Window(
        Const(LEXICON_RU['/order_info']),
        Const('Ваш заказ:'),
        List(
            Format('✅ {item.rent.name} - {item.quantity} {item.value} ({item.summa} руб.)'),
            items='orders',
        ),
        keyboards.return_to_category_keyboard(selected.on_chosen_return_to_category),
        getter=getters.get_all_orders,
        state=states.OrderRent.order_info
    )


async def on_process_result(start_data:Any,result:Any,manager:DialogManager):
    print('start_data:',start_data)
    print('result:',result)

    await manager.switch_to(BotMenu.select_categories)

async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer(LEXICON_RU['error_number'])


