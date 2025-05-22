from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from src.dialogs.bot_menu import selected, states, getters, keyboards
from src.lexicon.lexicon_ru import LEXICON_RU


def hello_window():
    return Window(
        Const(LEXICON_RU['/start']),
        keyboards.hello_keyboard(selected.on_hello),
        Cancel(Const('Exit')),
        state=states.BotMenu.hello,
    )

def categories_window():
    return Window(
        Const(LEXICON_RU['/categories']),
        keyboards.paginated_categories(selected.on_chosen_category),
        Cancel(Const('Exit')),
        state=states.BotMenu.select_categories,
        getter=getters.get_categories
    )