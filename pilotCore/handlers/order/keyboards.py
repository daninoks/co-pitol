from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.order import static_text as order_static
from pilotCore.handlers.order import manage_data as order_data
from pilotCore.handlers.driver import static_text as driver_static
from pilotCore.handlers.driver import manage_data as driver_data

from pilotCore.handlers.utils import scrolling_row



# def make_keyboard_broadcast() -> InlineKeyboardMarkup:
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 order_static.decline_order,
#                 callback_data=order_data.DECLINE_ORDER_BUTTON
#             ),
#             InlineKeyboardButton(
#                 order_static.accept_order,
#                 callback_data=order_data.ACCEPT_ORDER_BUTTON
#             )
#         ],
#     ]
#     return InlineKeyboardMarkup(buttons)


def make_keyboard_new_orders(orders_empty: bool, layout: list, decline_button: bool) -> InlineKeyboardMarkup:
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
        scroll_row = scrolling_row.scroll_layout_keyboard(
            layout,
            order_data.NOM_CB_PREFIX,
            order_data.NOM_PREV_ORDER,
            order_data.NOM_NEXT_ORDER,
        )

        lower_raw_buttons = []
        # Hide CANCEL if order Open.
        if decline_button:
            cancel_button = [
                InlineKeyboardButton(
                    order_static.decline_order,
                    callback_data=order_data.NOM_DECLINE_ORDER_BUTTON
                ),
            ]
            lower_raw_buttons.extend(cancel_button)

        accept_button = [
            InlineKeyboardButton(
                order_static.accept_order,
                callback_data=order_data.NOM_ACCEPT_ORDER_BUTTON
            )
        ]

        back_button = [
            InlineKeyboardButton(
                driver_static.back_driver_main,
                callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
            )
        ]

        lower_raw_buttons.extend(accept_button)
        buttons.append(scroll_row)
        buttons.append(lower_raw_buttons)
        buttons.append(back_button)
    return InlineKeyboardMarkup(buttons)


def make_keyboard_my_orders(orders_empty: bool, layout: list) -> InlineKeyboardMarkup:
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
        scroll_row = scrolling_row.scroll_layout_keyboard(
            layout,
            order_data.MOM_CB_PREFIX,
            order_data.MOM_PREV_ORDER,
            order_data.MOM_NEXT_ORDER,
        )
        buttons.append(scroll_row)

        lower_raw_buttons = [
            [
                # maybe HIDE instead?
                InlineKeyboardButton(
                    order_static.decline_order,
                    callback_data=order_data.MOM_DECLINE_ORDER_BUTTON
                ),
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
