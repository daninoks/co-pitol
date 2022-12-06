from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from pilotCore.handlers.welcome import static_text, manage_data




def make_keyboard_start_command() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                static_text.customer_button,
                callback_data=manage_data.CUSTOMER_BUTTON
            )
        ],
        [
            InlineKeyboardButton(
                static_text.driver_button,
                callback_data=manage_data.DRIVER_BUTTON
            ),
            # InlineKeyboardButton(
            #     static_text.operator_button,
            #     callback_data=manage_data.OPERATOR_BUTTON
            # )
        ],
        [
            InlineKeyboardButton(
                static_text.support_button,
                callback_data=manage_data.SUPPORT_BUTTON
            )
        ],
        # [
        #     InlineKeyboardButton(
        #         static_text.test_button,
        #         callback_data=manage_data.TEST_BUTTON
        #     )
        # ],
    ]
    return InlineKeyboardMarkup(buttons)
