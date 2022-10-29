from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.customer import static_text as customer_text
from pilotCore.handlers.customer import manage_data as customer_data

from pilotCore.handlers.goto import static_text as goto_text
from pilotCore.handlers.goto import manage_data as goto_data




def make_keyboard_customer_main() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                customer_text.list_routes_bt,
                callback_data=customer_data.LIST_ROUTES_CB
            )
        ],
        [
            InlineKeyboardButton(
                customer_text.set_route_alert_bt,
                callback_data=customer_data.SET_ROUTE_ALERT_CB
            )
        ],
        [
            InlineKeyboardButton(
                customer_text.customer_properties_bt,
                callback_data=customer_data.CUSTOMER_PROPERTIES_CB
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_customer_properties() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                customer_text.customer_set_name_bt,
                callback_data=customer_data.CUSTOMER_SET_NAME_CB
            )
        ],
        [
            InlineKeyboardButton(
                customer_text.customer_set_number_bt,
                callback_data=customer_data.CUSTOMER_SET_NUMBER_CB
            )
        ],
        [
            InlineKeyboardButton(
                goto_text.go_customer_main_bt,
                callback_data=goto_data.GO_CUSTOMER_MAIN_CB
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)
