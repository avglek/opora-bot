import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Column, Button
from aiogram_dialog.widgets.text import Format, Const

SCROLLING_HEIGHT = 6


def main_menu_keyboard(on_click):
    return Column(
        Select(
            Format('{item[0]}'),
            id = 's_main_menu',
            item_id_getter=operator.itemgetter(1),
            items = 'main_menu',
            on_click = on_click,
        )
    )

def add_contact_keyboard(on_click):
    return Column(
        Button(Const('Добавить контакт'), id = 'b_add_contact', on_click = on_click)
    )

def paginated_categories(on_click):
    return ScrollingGroup(
        Select(
            Format('{item.name}'),
            id = 's_scroll_categories',
            item_id_getter=operator.attrgetter('id'),
            items = 'categories',
            on_click = on_click,
        ),
        id = 'categories_ids',
        width = 1,
        height = SCROLLING_HEIGHT,
    )

def rents_keyboard(on_click):
    return Column(
        Select(
            Format('{item.name}'),
            id = 's_rents',
            item_id_getter=operator.attrgetter('id'),
            items = 'rents',
            on_click = on_click,
        )
    )
