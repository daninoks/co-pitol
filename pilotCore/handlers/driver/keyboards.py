from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.driver import static_text as driver_text
from pilotCore.handlers.driver import manage_data as driver_data
from pilotCore.handlers.utils import scrolling_row

from pilotCore.handlers.goto import static_text as goto_text
from pilotCore.handlers.goto import manage_data as goto_data




def make_keyboard_driver_main(newOrd_alert: str, myOrd_alert: str) -> InlineKeyboardMarkup:
    buttons = [
        # [
        #     # InlineKeyboardButton(
        #     #     driver_text.new_orders.format(alert = newOrd_alert),
        #     #     callback_data=driver_data.NEW_ORDERS_BUTTON
        #     # ),
        #     InlineKeyboardButton(
        #         driver_text.my_orders.format(alert = myOrd_alert),
        #         callback_data=driver_data.MY_ORDERS_BUTTON
        #     )
        # ],
        [
            # InlineKeyboardButton(
            #     driver_text.work_time,          # UPDATES EVERY DAY
            #     callback_data=driver_data.WORK_HOURS_BUTTON
            # ),
            # InlineKeyboardButton(
            #     driver_text.direction,          # UPDATES EVERY DAY
            #     callback_data=driver_data.DIRECTION_BUTTON
            # )

            # Set New Ride [My Ride]:
            InlineKeyboardButton(
                driver_text.my_rides_bt,
                callback_data=driver_data.MY_RIDES_BUTTON
            ),
        ],
        [
            InlineKeyboardButton(
                driver_text.car_settings,
                callback_data=driver_data.CAR_SETTINGS_BUTTON
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


def make_keyboard_my_rides(exists: bool, layout: list) -> InlineKeyboardMarkup:
    buttons = []
    if exists:
        scroll_row = scrolling_row.scroll_layout_keyboard(
            layout,
            driver_data.MR_CB_PREFIX,
            driver_data.MR_PREV_RIDE,
            driver_data.MR_NEXT_RIDE,
        )
        middle_row = [
            # Delete selected ride:
            InlineKeyboardButton(
                driver_text.my_rides_del_bt,
                callback_data=driver_data.MY_RIDES_DEL_BUTTON
            ),
            # # Edit selected ride:
            # InlineKeyboardButton(
            #     driver_text.my_rides_edit_bt,
            #     callback_data=driver_data.MY_RIDES_EDIT_BUTTON
            # ),
        ]
        buttons.append(scroll_row)
        buttons.append(middle_row)

    lower_row = [
        # Navigation here:
        [
            # Back driver main:
            InlineKeyboardButton(
                goto_text.go_driver_main_bt,
                callback_data=goto_data.GO_DRIVER_MAIN_CB
            ),
            # New ride:
            InlineKeyboardButton(
                driver_text.my_rides_new_bt,
                callback_data=driver_data.MY_RIDES_NEW_BUTTON
            ),
        ],
    ]
    buttons.extend(lower_row)
    return InlineKeyboardMarkup(buttons)

def make_keyboard_my_rides_time() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                driver_text.sel_direction_bt,
                callback_data=driver_data.SEL_DIRECTION_BUTTON
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_car_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                driver_text.mobile_number,
                callback_data=driver_data.MOBILE_NUMBER_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                driver_text.car_model,
                callback_data=driver_data.CAR_MODEL_BUTTON
            ),
            InlineKeyboardButton(
                driver_text.car_color,
                callback_data=driver_data.CAR_COLOR_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                driver_text.car_number,
                callback_data=driver_data.CAR_NUMBER_BUTTON
            ),
            InlineKeyboardButton(
                driver_text.car_seats,
                callback_data=driver_data.CAR_SEATS_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                goto_text.go_driver_main_bt,
                callback_data=goto_data.GO_DRIVER_MAIN_CB
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def make_keyboard_set_direction() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                driver_text.city_Yerevan,
                callback_data=driver_data.CITY_YEREVAN_BUTTON
            ),
            InlineKeyboardButton(
                driver_text.city_Ararat,
                callback_data=driver_data.CITY_ARARAT_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                driver_text.city_Ehegnadzor,
                callback_data=driver_data.CITY_EHEGNADZOR_BUTTON
            ),
            InlineKeyboardButton(
                driver_text.city_Jermuk,
                callback_data=driver_data.CITY_JERMUK_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                driver_text.del_city,
                callback_data=driver_data.DELETE_CITY_BUTTON
            ),
            # InlineKeyboardButton(
            #     driver_text.reverse_way,
            #     callback_data=driver_data.REVERSE_WAY_BUTTON
            # ),
        ],
        [
            InlineKeyboardButton(
                goto_text.go_my_rides_bt,
                callback_data=goto_data.GO_MY_RIDES_CB
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)

# First meet register form:
def make_keyboard_go_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                driver_text.car_settings,
                callback_data=driver_data.CAR_SETTINGS_BUTTON
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
