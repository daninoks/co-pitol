from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.customer import static_text as customer_text
from pilotCore.handlers.customer import manage_data as customer_data

from pilotCore.handlers.goto import static_text as goto_text
from pilotCore.handlers.goto import manage_data as goto_data

from pilotCore.handlers.utils import scrolling_row




def make_keyboard_customer_main() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                customer_text.list_routes_bt,
                callback_data=customer_data.LIST_ROUTES_CB
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         customer_text.set_route_alert_bt,
        #         callback_data=customer_data.SET_ROUTE_ALERT_CB
        #     )
        # ],
        [
            InlineKeyboardButton(
                customer_text.customer_properties_bt,
                callback_data=customer_data.CUSTOMER_PROPERTIES_CB
            )
        ],
        [
            InlineKeyboardButton(
                goto_text.go_start_over_bt,
                callback_data=goto_data.GO_START_OVER_CB
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


def make_keyboard_customer_list_routes(exists: bool, layout: list) -> InlineKeyboardMarkup:
    buttons = []
    if exists:
        scroll_row = scrolling_row.scroll_layout_keyboard(
            layout,
            customer_data.ROUTES_CB_PREFIX,
            customer_data.ROUTES_PREV_RIDE,
            customer_data.ROUTES_NEXT_RIDE,
        )
        middle_row = [
            # Select route:
            InlineKeyboardButton(
                customer_text.routes_select_bt,
                callback_data=customer_data.ROUTES_SELECT_BUTTON_CB
            )
        ]
        buttons.append(scroll_row)
        buttons.append(middle_row)

    lower_row = [
        # Navigation here:
        [
            # Back customer main:
            InlineKeyboardButton(
                goto_text.go_customer_main_bt,
                callback_data=goto_data.GO_CUSTOMER_MAIN_CB
            )
        ],
    ]
    buttons.extend(lower_row)
    return InlineKeyboardMarkup(buttons)



def make_keyboard_select_seats(seats) -> InlineKeyboardMarkup:
    buttons = [
        [   
            InlineKeyboardButton(
                "minus",
                callback_data=customer_data.CUSTOMER_SELECT_SEATS_MINUS_CB
            ),
            InlineKeyboardButton(
                f"{seats}",
                callback_data=customer_data.CUSTOMER_SELECT_SEATS_NUM_CB
            ),
            InlineKeyboardButton(
                "plus",
                callback_data=customer_data.CUSTOMER_SELECT_SEATS_PLUS_CB
            )
        ],
         [
            InlineKeyboardButton(
                customer_text.customer_select_seats_confirm_bt,
                callback_data=customer_data.CUSTOMER_SELECT_SEATS_CONFIRM_CB
            )
        ],
        [
            InlineKeyboardButton(
                goto_text.go_customer_list_routes_bt,
                callback_data=goto_data.GO_CUSTOMER_LIST_ROUTES_CB
            ),
            # InlineKeyboardButton(
            #     # customer_text.go_customer_main_bt,
            #     # callback_data=customer_data.GO_CUSTOMER_MAIN_CB
            # )
        ],
    ]
    return InlineKeyboardMarkup(buttons)





def make_keyboard_confirm_ride() -> InlineKeyboardMarkup:
    buttons = [
        [   
            InlineKeyboardButton(
                goto_text.go_customers_select_seats_bt,
                callback_data=goto_data.GO_CUSTOMER_SELECT_SEATS_CB
            ),
            InlineKeyboardButton(
                customer_text.customer_ride_confirm_bt,
                callback_data=customer_data.CUSTOMER_RIDE_CONFIRM_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)