import re

from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup,
    Bot, ForceReply
)
from telegram.ext import CallbackContext

from django_project.settings import TELEGRAM_TOKEN

from pilotCore import conversation
# from pilotCore import models
from pilotCore.handlers.driver import keyboards, manage_data, static_text
from pilotCore.models import User, Driver, DriverRides, DriverUtils
from pilotCore.handlers.order import handlers as order_handlers
from pilotCore.handlers.utils import scrolling_row


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



# def request_driver_access(update: Update, context: CallbackContext) -> int:
#     text = static_text.request_driver_access_text
#
#     context.bot.edit_message_text(
#         text=text,
#         chat_id=update.callback_query.message.chat.id,
#         message_id=update.callback_query.message.message_id,
#         reply_markup=keyboards.make_keyboard_driver_main(new_ord_field, my_ord_field),
#         parse_mode=ParseMode.HTML
#     )
#
#     return conversation.MAIN_TREE


def driver_main(update: Update, context: CallbackContext) -> int:
    """Handle DRIVER_BUTTON Query command"""
    """Filter New/Registred/Banned Users"""
    d, created = Driver.get_or_create_user(update, context)
    DriverUtils.set_last_msg_id(update, context)

    if d.registred == d.DRVR_ACCEPTED:
        text = static_text.driver_main_text.format(
            model = '-' if d.car_model is None else d.car_model,
            color = '-' if d.car_color is None else d.car_color,
            number = '-' if d.car_number is None else d.car_number,
            tel_number = '-' if d.mobile_number is None else d.mobile_number,
            seats = '-' if d.car_seats is None else d.car_seats,
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

    elif d.registred == d.DRVR_BANNED:
        text = static_text.driver_banned
        context.bot.edit_message_text(
            text=text,
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            reply_markup=keyboards.make_keyboard_back_main(),
            parse_mode=ParseMode.HTML
        )

    else:
        # New user register dialog:
        if created:
            text = static_text.driver_welcome_dialog
            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                reply_markup=keyboards.make_keyboard_go_settings(),
                parse_mode=ParseMode.HTML
            )
        else:
            text = static_text.driver_waiting_approval
            context.bot.edit_message_text(
                text=text,
                chat_id=update.callback_query.message.chat.id,
                message_id=update.callback_query.message.message_id,
                reply_markup=keyboards.make_keyboard_go_settings(),
                parse_mode=ParseMode.HTML
            )
    return conversation.MAIN_TREE



def my_rides(update: Update, context: CallbackContext) -> int:
    """Handle MY_RIDES_BUTTON Query"""

    call_back = update.callback_query.data
    d, _ = Driver.get_or_create_user(update, context)


    my_rides = list(
        DriverRides.objects.filter(
            user_id=update.callback_query.message.chat.id,
            status=DriverRides.RIDE_OPEN
        ).values(
            'user_id', 'username',
            'ride_id', 'departure_time', 'direction', 'seats_booked'
        )
    )

    if my_rides:
        rides_exists = True
        pages_max = len(my_rides) - 1
        du, _ = DriverUtils.get_or_create_user(update, context)
        current_page = du.myrides_page

        if call_back == manage_data.MR_NEXT_RIDE:
            current_page = DriverUtils.set_myride_page(update, context, pages_max, -2)
        if call_back == manage_data.MR_PREV_RIDE:
            current_page = DriverUtils.set_myride_page(update, context, pages_max, -1)
        if call_back in manage_data.MR_DYNAMIC_CB_RIDE:
            print(re.sub(f'{manage_data.MR_CB_PREFIX}:', '', call_back))
            current_page = DriverUtils.set_myride_page(
                update,
                context,
                pages_max,
                int(re.sub(f'{manage_data.MR_CB_PREFIX}:', '', call_back))
            )
        # keyboard pages:
        pages_layout = scrolling_row.scroll_layout_handler(current_page, pages_max)
        # current page object:
        rideObj = my_rides[current_page]
        du.selected_ride_id = rideObj.get('ride_id')
        du.save()

        text = static_text.my_rides_text.format(
            ride_id = rideObj.get('ride_id'),
            dep_time = rideObj.get('departure_time'),
            direction = rideObj.get('direction'),
            booked_seats = rideObj.get('seats'),
            car_seats = rideObj.get('car_seats')
        )
    else:
        rides_exists = False
        pages_layout = None
        text = static_text.myrides_empty


    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_my_rides(rides_exists, pages_layout),
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.RIDES_CONV


def my_rides_edit(update: Update, context: CallbackContext) -> int:
    """Handle Query:
        MY_RIDES_NEW_BUTTON
        MY_RIDES_EDIT_BUTTON
        MY_RIDES_DEL_BUTTON
    """
    text = 'my rides_edit menu'
    call_back = update.callback_query.data

    if call_back == manage_data.MY_RIDES_NEW_BUTTON:
        text = 'enter depart time'
        context.bot.edit_message_text(
            text=text,
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id,
            reply_markup=None,
            parse_mode=ParseMode.HTML
        )
    # if call_back ==


    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_my_rides(),
        parse_mode=ParseMode.HTML
    )
    return conversation.RIDES_CONV

def my_rides_time(update: Update, context: CallbackContext) -> int:

    field_data = update.message.text
    dr_time = DriverRides.new_time(update, context, field_data)

    text = f'Selected time: {dr_time}'

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
        reply_markup=keyboards.my_rides_time(),
        parse_mode=ParseMode.HTML
    )
    return conversation.RIDES_CONV

def set_direction(update: Update, context: CallbackContext) -> int:
    """Set DIRECTION_BUTTON Query"""
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
    return conversation.RIDES_CONV


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
            conversation.NUMBER_CONV,
            converstion.MOBILE_NUMBER_CONV
    """
    d, _ = Driver.get_or_create_user(update, context)
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



### OLD
# def set_hours(update: Update, context: CallbackContext) -> int:
#     """Set driver working schedule handler"""
#     field_data = update.message.text
#
#     if re.match('^([0-9][0-9]:[0-9][0-9]-[0-9][0-9]:[0-9][0-9])$', field_data):
#         updating_field = {
#             'name': 'work_hours',
#             'data': field_data
#         }
#         d = Driver.update_field(update, context, updating_field)
#         text = static_text.set_hours_text.format(
#             hours = getattr(d, updating_field.get('name'))
#         )
#         redirection = conversation.MAIN_TREE
#     else:
#         text = static_text.set_hours_text.format(
#             hours = '!WRONG FORMAT!'
#         )
#         redirection = conversation.HOURS_CONV
#
#     Bot(TELEGRAM_TOKEN).deleteMessage(
#         chat_id=update.message.chat.id,
#         message_id=update.message.message_id,
#         timeout=None
#     )
#
#     du, _ = DriverUtils.get_or_create_user(update, context)
#
#     context.bot.edit_message_text(
#         text=text,
#         chat_id=update.message.chat.id,
#         message_id=du.last_msg_id,
#         reply_markup=keyboards.make_keyboard_back_driver_main(),
#         parse_mode=ParseMode.MARKDOWN
#     )
#     return redirection

### OLD
# def set_direction(update: Update, context: CallbackContext) -> int:
#     """Set DIRECTION_BUTTON Query"""
#     d, _ = Driver.get_or_create_user(update, context)
#     call_back = update.callback_query.data
#
#     if d.direction is None or d.direction == '':
#         text = static_text.set_direction_empty
#     else:
#         text = d.direction
#
#     if call_back in manage_data.CITIES_CALLBACK:
#         field_data = manage_data.CITIES_CALLBACK[call_back]
#         d = Driver.add_direction(field_data, update, context)
#         text = d.direction
#     else:
#         if call_back == manage_data.DELETE_CITY_BUTTON:
#             d = Driver.remove_last_direction(update, context)
#             text = d.direction
#
#     context.bot.edit_message_text(
#         text=text,
#         chat_id=update.callback_query.message.chat.id,
#         message_id=update.callback_query.message.message_id,
#         reply_markup=keyboards.make_keyboard_set_direction(),
#         parse_mode=ParseMode.HTML
#     )
#     return conversation.MAIN_TREE




def bot_actions_set(update: Update, context: CallbackContext, field_name: str) -> None:
    """Repeatable actions for set handlers"""
    updating_field = {
        'name': field_name,
        'data': update.message.text
    }

    d = Driver.update_field(update, context, updating_field)

    text = static_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )

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
    return conversation.MAIN_TREE

def set_model(update: Update, context: CallbackContext) -> int:
    """Set car model handler"""
    bot_actions_set(update, context, 'car_model')

def set_seats(update: Update, context: CallbackContext) -> int:
    """Set car seats handler"""
    bot_actions_set(update, context, 'car_seats')

def set_color(update: Update, context: CallbackContext) -> int:
    """Set car color handler"""
    bot_actions_set(update, context, 'car_color')

def set_number(update: Update, context: CallbackContext) -> int:
    """Set car number handler"""
    bot_actions_set(update, context, 'car_number')

def set_mobile_number(update: Update, context: CallbackContext) -> int:
    """Set Driver mobile number handler"""
    bot_actions_set(update, context, 'mobile_number')
