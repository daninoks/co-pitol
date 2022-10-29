from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.goto import static_text, manage_data




def make_keyboard_go_start_over() -> InlineKeyboardMarkup:
    """Go to start_over [welcome_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_start_over_bt,
                callback_data=manage_data.GO_START_OVER_CB
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_go_driver_main() -> InlineKeyboardMarkup:
    """Go to driver_main [driver_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_driver_main_bt,
                callback_data=manage_data.GO_DRIVER_MAIN_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_go_my_rides() -> InlineKeyboardMarkup:
    """Go to my_rides [driver_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_my_rides_bt,
                callback_data=manage_data.GO_MY_RIDES_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_go_car_settings() -> InlineKeyboardMarkup:
    """Go to car_settings [driver_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_car_settings_bt,
                callback_data=manage_data.GO_CAR_SETTING_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_go_customer_mian() -> InlineKeyboardMarkup:
    """Go to customer_main [customer_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_customer_main_bt,
                callback_data=manage_data.GO_CUSTOMER_MAIN_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_go_customer_propeties() -> InlineKeyboardMarkup:
    """Go to customer_properties [customer_handlers]"""
    buttons = [
        [
            InlineKeyboardButton(
                static_text.go_customer_properties_bt,
                callback_data=manage_data.GO_CUSTOMER_PROPERTIES_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)
