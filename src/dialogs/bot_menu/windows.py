from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, Back
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.text import Const, Format
from src.dialogs.bot_menu import selected, states, getters, keyboards
from src.lexicon.lexicon_ru import LEXICON_RU, CONST_BACK

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
        Cancel(Const('Exit')),
        state=states.BotMenu.select_categories,
        getter=getters.get_categories
    )

def rents_window() -> Window:
    return Window(
        Const(LEXICON_RU['/rents']),
        keyboards.rents_keyboard(selected.on_chosen_rents),
        Back(Const(CONST_BACK)),
        Cancel(Const('Exit')),
        state=states.BotMenu.select_rents,
        getter=getters.get_rents
    )

def rent_info_window() -> Window:
    return Window(
        Format('{rent_info.name}'),
        Format('{rent_info.description}'),
        DynamicMedia(selector='photo'),
        Back(Const(CONST_BACK)),
        Cancel(Const('Exit')),
        state=states.BotMenu.rent_info,
        getter=getters.get_rent_info
    )

def add_contact_window()-> Window:
    return Window(
        Const(LEXICON_RU['/add_contact']),
        keyboards.add_contact_keyboard(selected.on_chosen_add_contact),
        Back(Const(CONST_BACK)),
        Cancel(Const('Exit')),
        state=states.MessageGroup.add_contact
    )