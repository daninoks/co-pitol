import time
import re

from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    Bot
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from django.db.models import Q

from django_project.settings import TELEGRAM_TOKEN

from pilotCore import conversation
from pilotCore.models import (
    Customer, CustomerRides, CustomerUtils,
    Driver, DriverRides,
    Order
)

from pilotCore.handlers.customer import keyboards as customer_keyboards
from pilotCore.handlers.customer import manage_data as customer_data
from pilotCore.handlers.customer import static_text as customer_text
from pilotCore.handlers.driver import static_text as driver_text
from pilotCore.handlers.goto import keyboards as goto_keyboards

from pilotCore.handlers.utils import scrolling_row



def customer_main(update: Update, context: CallbackContext) -> int:
    """Customer main page"""
    # Make 1st after customer confirmation.
    c, c_created = Customer.get_or_create_user(update, context)
    cr, _ = CustomerRides.get_or_create_user(update, context)

    # Set last message_id:
    CustomerUtils.set_last_msg_id(update, context)

    # Welcome states:
    if c.registred == c.CSTMR_ACCEPTED:
        text = customer_text.customer_main_tx
        keyboard = customer_keyboards.make_keyboard_customer_main()
    elif c.registred == c.CSTMR_BANNED:
        text = customer_text.customer_banned_tx
        keyboard = None
    else:
        if c_created:
            text = customer_text.customer_welcome_dialog_tx
        else:
            text = customer_text.customer_waiting_aproval_tx
        keyboard = goto_keyboards.make_keyboard_go_start_over()

    # Disaplay info about selected ride:
    if cr.ride_id_booked != None:
        dr = DriverRides.get_dr_by_ride_id(cr.ride_id_booked)
        text = customer_text.customer_main_ride_booked_tx.format(
            ride_id=dr.ride_id,
            dep_time=dr.departure_time,
            direction=dr.direction,
            seats_booked=cr.seats_booked
        )

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.MAIN_TREE




def customer_properties(update: Update, context: CallbackContext) -> int:
    """
    Customer properties page with keyboard, also cover redirection:

    Redirects CUSTOMER_SET_NAME_CB and CUSTOMER_SET_NUMBER_CB to
    message field capture function:
        conversation.CUSTOMER_SET_NAME_CONV
        conversation.CUSTOMER_SET_NUMBER_CONV
    """
    # Also redirects here at registaration.
    c, _ = Customer.get_or_create_user(update, context)
    call_back = update.callback_query.data
    call_back_sub = re.sub('_CB', '', call_back).lower()
    # Customer real_name and mobile_number redirection:
    if call_back in customer_data.REPLY_HANDLESR:
        if getattr(c, call_back_sub) is None:
            text = customer_text.customer_properties_empty_dt[call_back_sub]
        else:
            text = customer_text.customer_properties_set_dt[call_back_sub].format(
                cb_var = getattr(c, call_back_sub)
            )
        redirect_keyboard = goto_keyboards.make_keyboard_go_customer_propeties()
        redirect_conv = customer_data.CONVERSATION_REDIRECT[call_back]
    else:
        cef = customer_text.customer_empty_fields
        text = customer_text.customer_properties_tx.format(
            name = cef if c.real_name is None else c.real_name,
            tel = cef if c.mobile_number is None else c.mobile_number
        )
        redirect_keyboard = customer_keyboards.make_keyboard_customer_properties()
        redirect_conv = conversation.MAIN_TREE

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=redirect_keyboard,
        parse_mode=ParseMode.HTML
    )
    return redirect_conv




def customer_actions_set(update: Update, context: CallbackContext, field_name: str) -> None:
    """ Repeatable actions for set handlers """
    updating_field = {
        'name': field_name,
        'data': update.message.text
    }
    # Model updates selected field:
    c = Customer.update_field(update, context, updating_field)
    text = customer_text.customer_properties_set_dt.get(updating_field.get('name')).format(
        cb_var = updating_field.get('data')
    )
    # Deleting user message:
    Bot(TELEGRAM_TOKEN).deleteMessage(
        chat_id=update.message.chat.id,
        message_id=update.message.message_id,
        timeout=None
    )
    # Get Query message_id to update:
    cu, _ = CustomerUtils.get_or_create_user(update, context)
    # Edit previous message:
    context.bot.edit_message_text(
        text=text,
        chat_id=update.message.chat.id,
        message_id=cu.last_msg_id,
        reply_markup=goto_keyboards.make_keyboard_go_customer_propeties(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE

def set_customer_name(update: Update, context: CallbackContext) -> int:
    """Set car model handler"""
    customer_actions_set(update, context, 'real_name')

def set_customer_number(update: Update, context: CallbackContext) -> int:
    """Set car model handler"""
    customer_actions_set(update, context, 'mobile_number')




def update_availible_routes_list(update) -> list:
    """Update list of pages for customer_list_routes from DriverRides"""
    availible_routes_open = list(
        DriverRides.objects.filter(
            status=DriverRides.RIDE_OPEN
        ).values(
            'user_id', 'username',
            'ride_id', 'departure_time', 'direction', 'seats_booked'
        )
    )
    return availible_routes_open



def customer_list_routes(update: Update, context: CallbackContext) -> int:
    """List all DriversRoutes. Provides selection of trip and booking"""

    call_back = update.callback_query.data

    # scrolling_raw_content
    table_content = update_availible_routes_list(update)

    # If Driver have active rides it apply scroll raw:
    if table_content:
        rides_exists = True
        pages_max = len(table_content) - 1

        class_object, _ = CustomerUtils.get_or_create_user(update, context)
        current_page = class_object.myrides_page
        if call_back == customer_data.ROUTES_NEXT_RIDE:
            current_page = CustomerUtils.set_myride_page(class_object, pages_max, -2)
        if call_back == customer_data.ROUTES_PREV_RIDE:
            current_page = CustomerUtils.set_myride_page(class_object, pages_max, -1)
        if call_back in customer_data.ROUTES_DYNAMIC_CB_RIDE:
            #print(re.sub(f'{customer_data.ROUTES_CB_PREFIX}:', '', call_back))
            current_page = CustomerUtils.set_myride_page(
                class_object,
                pages_max,
                int(re.sub(f'{customer_data.ROUTES_CB_PREFIX}:', '', call_back))
            )
        # keyboard pages:
        pages_layout = scrolling_row.scroll_layout_handler(current_page, pages_max)
        # current page object:
        if current_page <= int(len(table_content) - 1):
            table_content_obj = table_content[current_page]
        else:
             table_content_obj = table_content[0]
        class_object.selected_ride_id = table_content_obj.get('ride_id')
        class_object.save()
        
        d = Driver.get_d_by_user_id(table_content_obj.get('user_id'))
        dr = DriverRides.get_dr_by_ride_id(table_content_obj.get('ride_id'))


        text = driver_text.my_rides_text.format(
            ride_id = table_content_obj.get('ride_id'),
            dep_time = table_content_obj.get('departure_time'),
            direction = table_content_obj.get('direction'),
            booked_seats = dr.seats_booked,
            car_seats = d.car_seats
        )
    else:
        rides_exists = False
        pages_layout = None
        text = driver_text.myrides_empty

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=customer_keyboards.make_keyboard_customer_list_routes(rides_exists, pages_layout),
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.MAIN_TREE





def customer_select_seats(update: Update, context: CallbackContext) -> int:
    """Select number of seats and final ride confirm"""

    call_back = update.callback_query.data
    warning = ''

    cu, _ = CustomerUtils.get_or_create_user(update, context)
    cr, _ = CustomerRides.get_or_create_user(update, context)
    dr = DriverRides.get_dr_by_ride_id(cu.selected_ride_id)
    d = Driver.get_d_by_user_id(cu.user_id)

    # # Set customer selected ride:
    # cr.seats_booked = cu.selected_ride_id
    # cr.save()

    if call_back == customer_data.CUSTOMER_SELECT_SEATS_MINUS_CB:
        if cr.seats_booked == 1:
            warning = customer_text.select_seats_min_warning_mess
        else:
            cr.seats_booked -= 1
            cr.save()
            
    if call_back == customer_data.CUSTOMER_SELECT_SEATS_PLUS_CB:
        if cr.seats_booked == d.car_seats:
            warning = customer_text.select_seats_max_warning_mess.format(
                car_seats = d.car_seats
            )
        else:
            cr.seats_booked += 1
            cr.save()

    keyboard = customer_keyboards.make_keyboard_select_seats(cr.seats_booked)
    
    if call_back == customer_data.CUSTOMER_SELECT_SEATS_CONFIRM_CB:
        # For now support only one selected ride.
        # Link Customer to selected Ride.
        cr.ride_id_booked = cu.selected_ride_id
        cr.save()
        dr.seats_booked = dr.seats_booked + cr.seats_booked
        dr.save()

        warning = customer_text.select_seats_warning_mess
        keyboard = customer_keyboards.make_keyboard_confirm_ride()

    text = customer_text.customer_select_seats_tx.format(
        ride_id = dr.ride_id,
        dep_time = dr.departure_time,
        direction = dr.direction,
        sel_seats = cr.seats_booked,
        avail_seats = d.car_seats - dr.seats_booked,
        warning_mess = warning
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.MAIN_TREE






