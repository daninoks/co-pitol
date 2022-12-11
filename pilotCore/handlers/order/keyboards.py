# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# from pilotCore.handlers.order import static_text as order_static
# from pilotCore.handlers.order import manage_data as order_data
# from pilotCore.handlers.driver import static_text as driver_static
# from pilotCore.handlers.driver import manage_data as driver_data

# from pilotCore.handlers.utils import scrolling_row



# def make_keyboard_broadcast() -> InlineKeyboardMarkup:
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 order_static.go_to_new_orders,
#                 callback_data=order_data.GO_TO_NEW_ORDERS
#             )
#         ],
#     ]
#     return InlineKeyboardMarkup(buttons)


# def make_keyboard_new_orders(orders_empty: bool, layout: list, decline_button: bool) -> InlineKeyboardMarkup:
#     if orders_empty:
#         buttons = [
#             [
#                 InlineKeyboardButton(
#                     driver_static.back_driver_main,
#                     callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
#                 )
#             ],
#         ]
#     else:
#         # Hide CANCEL if order Open and ACCEPT if order Pending:.
#         middle_row = []
#         if decline_button:
#             cancel_button = [
#                 InlineKeyboardButton(
#                     order_static.decline_order,
#                     callback_data=order_data.NOM_DECLINE_ORDER_BUTTON
#                 ),
#             ]
#             middle_row.extend(cancel_button)
#         else:
#             accept_button = [
#                 InlineKeyboardButton(
#                     order_static.accept_order,
#                     callback_data=order_data.NOM_ACCEPT_ORDER_BUTTON
#                 )
#             ]
#             middle_row.extend(accept_button)

#         scroll_row = scrolling_row.scroll_layout_keyboard(
#             layout,
#             order_data.NOM_CB_PREFIX,
#             order_data.NOM_PREV_ORDER,
#             order_data.NOM_NEXT_ORDER,
#         )
#         back_button = [
#             InlineKeyboardButton(
#                 driver_static.back_driver_main,
#                 callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
#             )
#         ]

#         buttons = []
#         buttons.append(scroll_row)
#         buttons.append(middle_row)
#         buttons.append(back_button)
#     return InlineKeyboardMarkup(buttons)


# def make_keyboard_my_orders(orders_empty: bool, layout: list) -> InlineKeyboardMarkup:
#     if orders_empty:
#         buttons = [
#             [
#                 InlineKeyboardButton(
#                     driver_static.back_driver_main,
#                     callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
#                 )
#             ],
#         ]
#     else:
#         buttons = []
#         scroll_row = scrolling_row.scroll_layout_keyboard(
#             layout,
#             order_data.MOM_CB_PREFIX,
#             order_data.MOM_PREV_ORDER,
#             order_data.MOM_NEXT_ORDER,
#         )
#         buttons.append(scroll_row)

#         middle_row = [
#             [
#                 # maybe HIDE instead?
#                 InlineKeyboardButton(
#                     order_static.decline_order,
#                     callback_data=order_data.MOM_DECLINE_ORDER_BUTTON
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     driver_static.back_driver_main,
#                     callback_data=driver_data.BACK_DRIVER_MAIN_BUTTON
#                 )
#             ],
#         ]
#         buttons.extend(middle_row)
#     return InlineKeyboardMarkup(buttons)
