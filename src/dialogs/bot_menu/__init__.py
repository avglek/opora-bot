from aiogram_dialog import Dialog

from src.dialogs.bot_menu import windows


def bot_menu_dialog():
    return [
        Dialog(
            windows.main_menu_window(),
            windows.categories_window(),
            windows.rents_window(),
            windows.rent_info_window(),
            windows.price_info_window(),
            windows.order_rent_window(),
            #
            #on_process_result=windows.on_process_result,
        ),
        Dialog(
            #windows.confirm_buy_window(),
            windows.add_to_order_window(),
            windows.order_window(),
            windows.order_complete_window(),
        ),
        Dialog(
            windows.add_contact_window(),
        )

        ]