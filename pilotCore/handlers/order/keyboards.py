from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.order import static_text as order_static
from pilotCore.handlers.order import manage_data as order_data
from pilotCore.handlers.driver import static_text as driver_static
from pilotCore.handlers.driver import manage_data as driver_data




def make_keyboard_broadcast() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                order_static.decline_order,
                callback_data=order_data.DECLINE_ORDER_BUTTON
            ),
            InlineKeyboardButton(
                order_static.accept_order,
                callback_data=order_data.ACCEPT_ORDER_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_new_orders(orders_empty: bool, layout: list) -> InlineKeyboardMarkup:
    if orders_empty:
        buttons = [
            [
                InlineKeyboardButton(
                    driver_static.back_driver_main,
                    callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
                )
            ],
        ]
    else:
        buttons = []
        upper_row = []

        left_button = [
            InlineKeyboardButton(
                order_static.prev_order,
                callback_data=order_data.PREV_ORDER
            ),
        ]
        upper_row.extend(left_button)

        number_buttons_layout = []
        for value in layout:
            if value != '\U000025CF':
                value_view = int(value) + 1
            else:
                value_view = value
            number_buttons_layout.append(
                InlineKeyboardButton(
                    str(value_view),
                    callback_data=f'cb:{value}'
                ),
            )
        upper_row.extend(number_buttons_layout)

        right_button = [
            InlineKeyboardButton(
                order_static.next_order,
                callback_data=order_data.NEXT_ORDER
            )
        ]
        upper_row.extend(right_button)
        buttons.append(upper_row)

        lower_raw_buttons = [
            [
                # maybe HIDE instead?
                # InlineKeyboardButton(
                #     order_static.decline_order,
                #     callback_data=order_data.DECLINE_ORDER_BUTTON
                # ),
                InlineKeyboardButton(
                    order_static.accept_order,
                    callback_data=order_data.ACCEPT_ORDER_BUTTON
                )
            ],
            [
                InlineKeyboardButton(
                    driver_static.back_driver_main,
                    callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
                )
            ],
        ]
        buttons.extend(lower_raw_buttons)
    return InlineKeyboardMarkup(buttons)
