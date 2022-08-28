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


def make_keyboard_new_orders(orders_empty: bool) -> InlineKeyboardMarkup:
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
        buttons = [
            [
                InlineKeyboardButton(
                    order_static.prev_order,
                    callback_data=order_data.PREV_ORDER
                ),
                InlineKeyboardButton(
                    order_static.next_order,
                    callback_data=order_data.NEXT_ORDER
                )
            ],
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
    return InlineKeyboardMarkup(buttons)
