from aiogram.fsm.state import StatesGroup, State


class BotMenu(StatesGroup):
    price_info = State()
    main_menu = State()
    select_categories = State()
    select_rents = State()
    rent_info = State()
    order_rent = State()

class OrderRent(StatesGroup):
    add_to_order = State()
    order_info = State()

class MessageGroup(StatesGroup):
    add_contact = State()
