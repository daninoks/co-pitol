from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.driver import static_text, manage_data
from pilotCore.handlers.utils import scrolling_row





def make_keyboard_driver_main(newOrd_alert: str, myOrd_alert: str) -> InlineKeyboardMarkup:
    buttons = [
        # [
        #     # InlineKeyboardButton(
        #     #     static_text.new_orders.format(alert = newOrd_alert),
        #     #     callback_data=manage_data.NEW_ORDERS_BUTTON
        #     # ),
        #     InlineKeyboardButton(
        #         static_text.my_orders.format(alert = myOrd_alert),
        #         callback_data=manage_data.MY_ORDERS_BUTTON
        #     )
        # ],
        [
            # InlineKeyboardButton(
            #     static_text.work_time,          # UPDATES EVERY DAY
            #     callback_data=manage_data.WORK_HOURS_BUTTON
            # ),
            # InlineKeyboardButton(
            #     static_text.direction,          # UPDATES EVERY DAY
            #     callback_data=manage_data.DIRECTION_BUTTON
            # )

            # Set New Ride [My Ride]:
            InlineKeyboardButton(
                static_text.my_rides_bt,
                callback_data=manage_data.MY_RIDES_BUTTON
            ),
        ],
        [
            InlineKeyboardButton(
                static_text.car_settings,
                callback_data=manage_data.CAR_SETTINGS_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.back_main,
                callback_data=manage_data.BACK_MAIN_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_my_rides(exists: bool, layout: list) -> InlineKeyboardMarkup:
    buttons = []
    if exists:
        scroll_row = scrolling_row.scroll_layout_keyboard(
            layout,
            manage_data.MR_CB_PREFIX,
            manage_data.MR_PREV_RIDE,
            manage_data.MR_NEXT_RIDE,
        )
        middle_row = [
            # Delete selected ride:
            InlineKeyboardButton(
                static_text.my_rides_del_bt,
                callback_data=manage_data.MY_RIDES_DEL_BUTTON
            ),
            # Edit selected ride:
            InlineKeyboardButton(
                static_text.my_rides_edit_bt,
                callback_data=manage_data.MY_RIDES_EDIT_BUTTON
            ),
        ]
        buttons.append(scroll_row)
        buttons.append(middle_row)

    lower_row = [
        # Navigation here:
        [
            # New ride:
            InlineKeyboardButton(
                static_text.my_rides_new_bt,
                callback_data=manage_data.MY_RIDES_NEW_BUTTON
            ),
        ],
        [
            # Back driver main:
            InlineKeyboardButton(
                static_text.back_driver_main,
                callback_data=manage_data.BACK_DRIVER_MAIN_BUTTON
            )
        ],
    ]
    buttons.extend(lower_row)
    return InlineKeyboardMarkup(buttons)

def make_keyboard_my_rides_time() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.sel_direction_bt,
                callback_data=manage_data.SEL_DIRECTION_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


# def make_keyboard_new_ride_location() -> InlineKeyboardMarkup:
#     buttons = [
#         # Navigation here:
#         [
#             # Edit selected ride:
#             InlineKeyboardButton(
#                 static_text.mobile_number,
#                 callback_data=manage_data.MOBILE_NUMBER_BUTTON
#             )
#         ],
#         [
#             # Back drier main:
#             InlineKeyboardButton(
#                 static_text.back_driver_main,
#                 callback_data=manage_data.BACK_DRIVER_MAIN_BUTTON
#             )
#         ],
#     ]
#     return InlineKeyboardMarkup(buttons)




def make_keyboard_car_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.mobile_number,
                callback_data=manage_data.MOBILE_NUMBER_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.car_model,
                callback_data=manage_data.CAR_MODEL_BUTTON
            ),
            InlineKeyboardButton(
                static_text.car_color,
                callback_data=manage_data.CAR_COLOR_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.car_number,
                callback_data=manage_data.CAR_NUMBER_BUTTON
            ),
            InlineKeyboardButton(
                static_text.car_seats,
                callback_data=manage_data.CAR_SEATS_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.back_driver_main,
                callback_data=manage_data.BACK_DRIVER_MAIN_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_set_direction() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.city_Yerevan,
                callback_data=manage_data.CITY_YEREVAN_BUTTON
            ),
            InlineKeyboardButton(
                static_text.city_Ararat,
                callback_data=manage_data.CITY_ARARAT_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.city_Ehegnadzor,
                callback_data=manage_data.CITY_EHEGNADZOR_BUTTON
            ),
            InlineKeyboardButton(
                static_text.city_Jermuk,
                callback_data=manage_data.CITY_JERMUK_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.del_city,
                callback_data=manage_data.DELETE_CITY_BUTTON
            ),
            # InlineKeyboardButton(
            #     static_text.reverse_way,
            #     callback_data=manage_data.REVERSE_WAY_BUTTON
            # ),
        ],
        [
            InlineKeyboardButton(
                static_text.back_my_rides_bt,
                callback_data=manage_data.BACK_MY_RIDES_BUTTON
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# First meet register form:
def make_keyboard_go_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.car_settings,
                callback_data=manage_data.CAR_SETTINGS_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.back_main,
                callback_data=manage_data.BACK_MAIN_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)

# SOLO FORWARD BUTTONS:
# def make_keyboard_my_rides_time_confirm() -> InlineKeyboardMarkup:
#     """Confirm depart time and go directions"""
#     buttons = [
#         [
#             InlineKeyboardButton(
#                 static_text.my_rides_time_confirm,
#                 callback_data=manage_data.BACK_CAR_SETTING_BUTTON
#             )
#         ]
#     ]
#     return InlineKeyboardMarkup(buttons)

# SOLO BACK BUTTON KEYBOARDS:
def make_keyboard_back_car_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.back_car_settings,
                callback_data=manage_data.MY_RIDES_TIME_CONFIRM
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_back_driver_main() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.back_driver_main,
                callback_data=manage_data.BACK_DRIVER_MAIN_BUTTON
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def make_keyboard_back_main() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.back_main,
                callback_data=manage_data.BACK_MAIN_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)
