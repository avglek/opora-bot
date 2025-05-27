from aiogram.fsm.state import StatesGroup, State


class BotMenu(StatesGroup):
    main_menu = State()
    select_categories = State()
    select_rents = State()
    rent_info = State()

class MessageGroup(StatesGroup):
    add_contact = State()
