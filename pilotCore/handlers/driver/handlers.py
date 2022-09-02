import re

from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup,
    Bot, ForceReply
)
from telegram.ext import CallbackContext

from django_project.settings import TELEGRAM_TOKEN

from pilotCore import conversation
from pilotCore.handlers.driver import keyboards, manage_data, static_text
from pilotCore.models import User, Driver, DriverUtils
from pilotCore.handlers.order import handlers as order_handlers


# wrong field allert
# Bot(TELEGRAM_TOKEN).answer_callback_query(
#     callback_query_id=update.callback_query.id,
#     text="TTTTTTTTTTTT",
#     show_alert=True
# )


def delete_missclicked_messages(update: Update, context: CallbackContext) -> None:
    """Deleting messages from User outside the input conversation"""
    DriverUtils.inc_counter(update, context)


    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )


def driver_main(update: Update, context: CallbackContext) -> int:
    """Handle DRIVER_BUTTON Query command"""
    d, _ = Driver.get_or_create_user(update, context)
    DriverUtils.set_last_msg_id(update, context)

    text = static_text.driver_main_text.format(
        hours = 'Please set in WORK TIME' if d.work_hours is None else d.work_hours,
        model = '-' if d.car_model is None else d.car_model,
        color = '-' if d.car_color is None else d.car_color,
        number = '-' if d.car_number is None else d.car_number,
        seats = '-' if d.car_seats is None else d.car_seats,
        direction = 'Set in DIRECTION' if d.direction is None or d.direction == '' else d.direction
    )

    # alert_symbol = u'\U000026A0 '
    new_ord_field = (
        '' if (new_ord_count := len(order_handlers.update_new_order_list(update))) == 0
        else f'[{new_ord_count}]'
    )
    my_ord_field = (
        '' if (my_ord_couter := len(order_handlers.update_my_order_list(update))) == 0
        else f'[{my_ord_couter}]'
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_driver_main(new_ord_field, my_ord_field),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE


def car_settings(update: Update, context: CallbackContext) -> int:
    """Handle CAR_SETTINGS Query command"""
    d, _ = Driver.get_or_create_user(update, context)

    text = static_text.car_settings_dynamic.format(
        mobile = '-' if d.mobile_number is None else d.mobile_number,
        model = '-' if d.car_model is None else d.car_model,
        color = '-' if d.car_color is None else d.car_color,
        number = '-' if d.car_number is None else d.car_number,
        seats = '-' if d.car_seats is None else d.car_seats,
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_car_settings(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE


def driver_preference(update: Update, context: CallbackContext) -> int:
    """Handle Query to converstion fields"""
    """
        Entry point to:
            conversation.HOURS_CONV,
            conversation.MODEL_CONV,
            conversation.SEATS_CONV,
            conversation.COLOR_CONV,
            conversation.NUMBER_CONV
    """
    d, exists = Driver.get_or_create_user(update, context)
    call_back = update.callback_query.data
    call_back_sub = re.sub('_BTTN', '', update.callback_query.data).lower()

    if call_back in manage_data.REPLY_HANDLESR:
        if getattr(d, call_back_sub) is None:
            text = static_text.driver_preference_none[call_back_sub]
        else:
            text = static_text.driver_preference_text[call_back_sub].format(
                cb_var = getattr(d, call_back_sub)
            )
        redirection = manage_data.CONVERSATION_REDIRECT[call_back]

    if redirection == conversation.HOURS_CONV:
        keyboard = keyboards.make_keyboard_back_driver_main()
    else:
        keyboard = keyboards.make_keyboard_back_car_settings()

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

    if redirection:
        return redirection
    else:
        return manage_data.MAIN_TREE




def set_hours(update: Update, context: CallbackContext) -> int:
    """Set driver working schedule handler"""
    field_data = update.message.text

    if re.match('^([0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9])$', field_data):
        updating_field = {
            'name': 'work_hours',
            'data': field_data
        }
        d = Driver.update_field(update, context, updating_field)
        text = static_text.set_hours_text.format(
            hours = getattr(d, updating_field.get('name'))
        )
        redirection = conversation.MAIN_TREE
    else:
        text = static_text.set_hours_text.format(
            hours = '!WRONG FORMAT!'
        )
        redirection = conversation.HOURS_CONV

    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )

    du, _ = DriverUtils.get_or_create_user(update, context)

    context.bot.edit_message_text(
        text=text,
        chat_id=update.message.chat.id,
        message_id=du.last_msg_id,
        reply_markup=keyboards.make_keyboard_back_driver_main(),
        parse_mode=ParseMode.MARKDOWN
    )
    return redirection


def set_direction(update: Update, context: CallbackContext) -> int:
    """Set directions"""
    d, _ = Driver.get_or_create_user(update, context)
    call_back = update.callback_query.data

    if d.direction is None or d.direction == '':
        text = static_text.set_direction_empty
    else:
        text = d.direction

    if call_back in manage_data.CITIES_CALLBACK:
        field_data = manage_data.CITIES_CALLBACK[call_back]
        d = Driver.add_direction(field_data, update, context)
        text = d.direction
    else:
        if call_back == manage_data.DELETE_CITY_BUTTON:
            d = Driver.remove_last_direction(update, context)
            text = d.direction

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_set_direction(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE




def bot_actions_set(update, context, text) -> None:
    """Repeatable actions for set handlers"""
    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )

    du, _ = DriverUtils.get_or_create_user(update, context)

    context.bot.edit_message_text(
        text=text,
        chat_id=update.message.chat.id,
        message_id=du.last_msg_id,
        reply_markup=keyboards.make_keyboard_back_car_settings(),
        parse_mode=ParseMode.HTML
    )

def set_model(update: Update, context: CallbackContext) -> int:
    """Set car model handler"""
    updating_field = {
        'name': 'car_model',
        'data': update.message.text
    }

    d = Driver.update_field(update, context, updating_field)

    text = static_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    bot_actions_set(update, context, text)
    return conversation.MAIN_TREE

def set_seats(update: Update, context: CallbackContext) -> int:
    """Set car seats handler"""
    updating_field = {
        'name': 'car_seats',
        'data': update.message.text
    }

    d = Driver.update_field(update, context, updating_field)

    text = static_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    bot_actions_set(update, context, text)
    return conversation.MAIN_TREE

def set_color(update: Update, context: CallbackContext) -> int:
    """Set car color handler"""
    updating_field = {
        'name': 'car_color',
        'data': update.message.text
    }

    d = Driver.update_field(update, context, updating_field)

    text = static_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    bot_actions_set(update, context, text)
    return conversation.MAIN_TREE

def set_number(update: Update, context: CallbackContext) -> int:
    """Set car number handler"""
    updating_field = {
        'name': 'car_number',
        'data': update.message.text
    }

    d = Driver.update_field(update, context, updating_field)

    text = static_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    bot_actions_set(update, context, text)
    return conversation.MAIN_TREE
