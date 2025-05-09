from typing import Any

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row,Select,Column
from aiogram_dialog.widgets.text import Const, Format

from ..keyboards.keyboards import Home
from ..lexicon.lexicon_ru import LEXICON_RU, BUTTONS_START, BUTTONS_START_2


class DialogSG(StatesGroup):
    home = State()
    rental = State()
    category = State()
    subcategory = State()
    item = State()


async def go_back(callback: CallbackQuery, button: Button,
                  manager: DialogManager):
    await manager.back()


async def go_home(callback: CallbackQuery, button: Button,
                  manager: DialogManager):
    await manager.switch_to(DialogSG.home)

async def go_next(callback: CallbackQuery, button: Button,
                  manager: DialogManager):
    await manager.next()

async def on_item_selected(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    selected_item: str,
):
    print(f"Selected item: {selected_item}")
    await callback.answer(selected_item)


dialog = Dialog(
    Window(
        Const(LEXICON_RU['/start']),
        Column(
            Select(
                Format("{item}"),
                id="start",
                items=BUTTONS_START_2,
                item_id_getter=lambda item: item,
                on_click=on_item_selected,
            )
        ),
        state=DialogSG.home,
    ),
    Window(
        Const("Rental"),
        Row(
            Button(Const("Back"), id="back2", on_click=go_back),
            Button(Const("Next"), id="next2", on_click=go_next),
        ),
        state=DialogSG.rental,
    ),
    Window(
        Const("Category"),
        Button(Const("Back"), id="back3", on_click=go_back),
        Button(Const("Next"), id="next3", on_click=go_next),
        state=DialogSG.category,
    ),
    Window(
        Const("Subcategory"),
        Button(Const("Back"), id="back4", on_click=go_back),
        Button(Const("Next"), id="next4", on_click=go_next),
        state=DialogSG.subcategory,
    ),
    Window(
        Const("Item"),
        Button(Const("Back"), id="back5", on_click=go_back),
        state=DialogSG.item,
    )
)
