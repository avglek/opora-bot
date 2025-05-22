from aiogram.fsm.state import StatesGroup, State


class BotMenu(StatesGroup):
    hello = State()
    select_categories = State()
    select_products = State()
    product_info = State()