import re
import logging

from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup,
    Bot, ForceReply
)
from telegram.ext import CallbackContext

from django_project.settings import TELEGRAM_TOKEN

from pilotCore import conversation
from pilotCore.handlers.driver import (
        keyboards as driver_keyboard,
        manage_data as driver_data,
        static_text as driver_text
)
from pilotCore.models import (
        User,
        Driver, DriverRides
)
from pilotCore.handlers.utils import scrolling_row

from pilotCore.handlers.order import handlers as order_handlers
from pilotCore.handlers.goto import keyboards as goto_keyboards




def delete_missclicked_messages(update: Update, context: CallbackContext) -> None:
    """ Deleting messages from User outside the input conversation """
    logging.debug("Message send by User - deleted")
    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )




def get_ride_list(update) -> list:
    """ List of all OPENed driver trips """
    rides_list = list(
        DriverRides.objects.filter(
            user_id=update.callback_query.message.chat.id,
            status=DriverRides.RIDE_OPEN
        ).values(
            'user_id', 'username',
            'ride_id', 'departure_time', 'direction', 'seats_booked', 'car_seats'
        )
    )
    return rides_list





def driver_main(update: Update, context: CallbackContext) -> int:
    """
    Handle DRIVER_BUTTON Query command
    Filter New/Registred/Banned User
    """
    d, created = Driver.get_or_create_user(update, context)
    User.set_last_msg_id(update, context)

    # Driver accepted by admin:
    if d.registred == d.DRVR_ACCEPTED:
        my_rides = get_ride_list(update)
        my_rides_block = ''
        if my_rides != []:
            my_rides_block += format('<code>\n\n      RIDES OWERIEW</code>')
        for item in my_rides:
            my_rides_block += driver_text.my_rides_overiew.format(
                ride_id = item.get('ride_id'),
                dep_time = item.get('departure_time'),
                direction = item.get('direction'),
                booked_seats = (
                        0 if item.get('seats_booked') == None
                        else item.get('seats_booked')
                ),
                car_seats = item.get('car_seats')
            )

        text = driver_text.driver_main_text.format(
            model = '-' if d.car_model is None else d.car_model,
            color = '-' if d.car_color is None else d.car_color,
            number = '-' if d.car_number is None else d.car_number,
            tel_number = '-' if d.mobile_number is None else d.mobile_number,
            seats = '-' if d.car_seats is None else d.car_seats,
            rides_overview = '' if my_rides_block == '' else my_rides_block
        )

        new_ord_field = (
            '' if (new_ord_count := len(order_handlers.update_new_order_list(update))) == 0
            else f'[{new_ord_count}]'
        )
        my_ord_field = (
            '' if (my_ord_couter := len(order_handlers.update_my_order_list(update))) == 0
            else f'[{my_ord_couter}]'
        )
        keyboard =driver_keyboard.make_keyboard_driver_main(new_ord_field, my_ord_field)

    # Driver banned by admin:
    elif d.registred == d.DRVR_BANNED:
        text = driver_text.driver_banned
        keyboard = goto_keyboards.make_keyboard_go_start_over()

    # New user register dialog:
    else:
        if created:
            text = driver_text.driver_welcome_dialog
        else:
            text = driver_text.driver_waiting_approval
        keyboard = goto_keyboards.make_keyboard_go_car_settings()

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE




def my_rides(update: Update, context: CallbackContext) -> int:
    """ Handle MY_RIDES_BUTTON Query """

    call_back = update.callback_query.data
    d, _ = Driver.get_or_create_user(update, context)

    my_rides = get_ride_list(update)

    # If Driver have active rides it apply scroll raw:
    if my_rides:
        rides_exists = True
        pages_max = len(my_rides) - 1

        u, _ = User.get_user_and_created(update, context)
        current_page = du.myrides_page
        if call_back == driver_data.MR_NEXT_RIDE:
            current_page = User.set_myride_page(u, pages_max, -2)
        if call_back == driver_data.MR_PREV_RIDE:
            current_page = User.set_myride_page(u, pages_max, -1)
        if call_back in driver_data.MR_DYNAMIC_CB_RIDE:
            #print(re.sub(f'{driver_data.MR_CB_PREFIX}:', '', call_back))
            current_page = User.set_myride_page(
                u,
                pages_max,
                int(re.sub(f'{driver_data.MR_CB_PREFIX}:', '', call_back))
            )
        # keyboard pages:
        pages_layout = scrolling_row.scroll_layout_handler(current_page, pages_max)
        # current page object:
        if current_page <= len(my_rides):
            rideObj = my_rides[current_page]
        else:
            rideObj = my_rides[0]
        
        du.selected_ride_id = rideObj.get('ride_id')
        du.save()

        text = driver_text.my_rides_text.format(
            ride_id = rideObj.get('ride_id'),
            dep_time = rideObj.get('departure_time'),
            direction = rideObj.get('direction'),
            booked_seats = (
                    0 if rideObj.get('seats_booked') == 'None' 
                    else rideObj.get('seats_booked')
            ),
            car_seats = rideObj.get('car_seats')
        )
    else:
        rides_exists = False
        pages_layout = None
        text = driver_text.myrides_empty

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=driver_keyboard.make_keyboard_my_rides(rides_exists, pages_layout),
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.RIDES_CONV


def my_rides_edit(update: Update, context: CallbackContext) -> int:
    """
    Handle Query:
        MY_RIDES_NEW_BUTTON
        MY_RIDES_EDIT_BUTTON
        MY_RIDES_DEL_BUTTON
    """
    text = 'my rides_edit menu'
    call_back = update.callback_query.data

    # Initiate New ride_id:
    if call_back == driver_data.MY_RIDES_NEW_BUTTON:
        dr, _ = DriverRides.create_new_ride_id(update, context)
        text = 'enter depart time'
        keyboard = None
    # Delete Selected ride:
    if call_back == driver_data.MY_RIDES_DEL_BUTTON:
        text = DriverRides.delete_ride(update, context)
        keyboard = goto_keyboards.make_keyboard_go_my_rides()

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    return conversation.RIDES_CONV


def my_rides_time(update: Update, context: CallbackContext) -> int:
    """ Set departure time """
    field_data = update.message.text
    u, _ = User.get_user_and_created(update, context)
    dr_time = DriverRides.new_time(du.new_ride_id, field_data)

    text = f'Selected time: {dr_time}'
    # Deleting user message:
    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )
    # Get Query message_id to update:
    u, _ = User.get_user_and_created(update, context)
    # Edit previous message:
    context.bot.edit_message_text(
        text=text,
        chat_id=update.message.chat.id,
        message_id=du.last_msg_id,
        reply_markup=driver_keyboard.make_keyboard_my_rides_time(),
        parse_mode=ParseMode.HTML
    )
    return conversation.RIDES_CONV


def set_direction(update: Update, context: CallbackContext) -> int:
    """Set DIRECTION_BUTTON Query"""
    # d, _ = DriverRides.get_or_create_user(update, context)
    u, _ = User.get_user_and_created(update, context)
    d = DriverRides.get_dr_by_ride_id(du.new_ride_id)

    call_back = update.callback_query.data

    if d.direction is None or d.direction == '':
        text = driver_text.set_direction_empty
    else:
        text = d.direction

    if call_back in driver_data.CITIES_CALLBACK:
        field_data = driver_data.CITIES_CALLBACK[call_back]
        d = DriverRides.add_direction(du.new_ride_id, field_data)
        text = d.direction

    if call_back == driver_data.DELETE_CITY_BUTTON:
        d = DriverRides.remove_last_direction(du.new_ride_id)
        text = d.direction

    if text == '':
        text = driver_text.set_direction_empty

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=driver_keyboard.make_keyboard_set_direction(),
        parse_mode=ParseMode.HTML
    )
    return conversation.RIDES_CONV


def car_settings(update: Update, context: CallbackContext) -> int:
    """Handle CAR_SETTINGS Query command"""
    d, _ = Driver.get_or_create_user(update, context)

    text = driver_text.car_settings_dynamic.format(
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
        reply_markup=driver_keyboard.make_keyboard_car_settings(),
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

    keyboard = goto_keyboards.make_keyboard_go_car_settings()
    if call_back in driver_data.REPLY_HANDLESR:
        if getattr(d, call_back_sub) is None:
            text = driver_text.driver_preference_none[call_back_sub]
        else:
            text = driver_text.driver_preference_text[call_back_sub].format(
                cb_var = getattr(d, call_back_sub)
            )
        redirection = driver_data.CONVERSATION_REDIRECT[call_back]
        if redirection == conversation.HOURS_CONV:
            keyboard = goto_keyboards.make_keyboard_go_driver_main()
    else:
        redirection = driver_data.MAIN_TREE

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )
    return redirection





def bot_actions_set(update: Update, context: CallbackContext, field_name: str) -> None:
    """Repeatable actions for set handlers"""
    updating_field = {
        'name': field_name,
        'data': update.message.text
    }
    # Model updates selected field:
    d = Driver.update_field(update, context, updating_field)

    text = driver_text.driver_preference_text.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    # Deleting user message:
    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )
    # Get Query message_id to update:
    u, _ = User.get_user_and_created(update, context)

    context.bot.edit_message_text(
        text=text,
        chat_id=update.message.chat.id,
        message_id=du.last_msg_id,
        reply_markup=goto_keyboards.make_keyboard_go_car_settings(),
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
