from aiogram_dialog.widgets.kbd import Button, Column,Select
from aiogram_dialog.widgets.text import Const, Format

from ..lexicon.lexicon_ru import BUTTONS_START


Home =Column(
    Select(
        Format("{item}"),
        id="start",
        items=BUTTONS_START.values(),
        item_id_getter=lambda x: x,
    )
)