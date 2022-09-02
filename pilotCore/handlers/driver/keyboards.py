from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.driver import static_text, manage_data





def make_keyboard_driver_main(newOrd_alert: str, myOrd_alert: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.new_orders.format(alert = newOrd_alert),
                callback_data=manage_data.NEW_ORDERS_BUTTON
            ),
            InlineKeyboardButton(
                static_text.my_orders.format(alert = myOrd_alert),
                callback_data=manage_data.MY_ORDERS_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.work_time,          # UPDATES EVERY DAY
                callback_data=manage_data.WORK_HOURS_BUTTON
            ),
            InlineKeyboardButton(
                static_text.direction,          # UPDATES EVERY DAY
                callback_data=manage_data.DIRECTION_BUTTON
            )
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


def make_keyboard_car_settings() -> InlineKeyboardMarkup:
    buttons = [
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
                static_text.conf_direction,
                callback_data=manage_data.BACK_DRIVER_MAIN_BUTTON
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)


# SOLO BACK BUTTON KEYBOARDS:
def make_keyboard_back_car_settings() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.back_car_settings,
                callback_data=manage_data.BACK_CAR_SETTING_BUTTON
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
