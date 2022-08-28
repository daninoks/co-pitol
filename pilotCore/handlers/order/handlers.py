from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup,
    Bot, ForceReply
)
from telegram.ext import CallbackContext

from pilotCore import conversation
from pilotCore.models import Order, Driver, DriverUtils
from pilotCore.handlers.order import static_text, manage_data, keyboards




def new_orders_menu(update: Update, context: CallbackContext) -> int:
    """Handle NEW_ORDERS_BUTTON Query command"""
    call_back = update.callback_query.data

    new_orders = list(Order.objects.filter(status=Order.ORD_OPEN).values(
        'order_id', 'departure_time', 'travel_direction',
        'seats', 'real_name', 'comment', 'status'
    ))

    if new_orders:
        ord_empty = False
        last_element = 0 if len(new_orders) == 0 else len(new_orders) - 1   # cant be 0 by if(?)
        no_num = DriverUtils.set_new_orders_num(update, context, last_element)

        du, _ = DriverUtils.get_or_create_user(update, context)
        no_page = du.new_orders_page

        if call_back == manage_data.NEXT_ORDER:
            no_page = DriverUtils.set_new_orders_page(update, context, 1)
        if call_back == manage_data.PREV_ORDER:
            no_page = DriverUtils.set_new_orders_page(update, context, -1)

        # current page object:
        orderObj = new_orders[no_page]

        # keyboard pages:
        current_page_marker = u'\U000025CF'
        page_selected = no_page
        pages_number = no_num

        pages_list = list(range(1, last_element + 1))
        max_listing_num = 5 if pages_number >= 5 else pages_number

        # if 




        text = static_text.new_orders_body.format(
            order_id = (
                'no info' if orderObj.get('order_id') is None
                else orderObj.get('order_id')
            ),
            daparture = (
                'no info' if orderObj.get('departure_time') is None
                else orderObj.get('departure_time')),
            direction = (
                'no info' if orderObj.get('travel_direction') is None
                else orderObj.get('travel_direction')
            ),
            name = (
                'no info' if orderObj.get('real_name') is None
                else orderObj.get('real_name')
            ),
            comment = (
                '' if orderObj.get('comment') == ''
                else u'\nU0001F4DC  comment:\n'+str(orderObj.get('comment'))
            ),
            seats = orderObj.get('seats')
        )
    else:
        ord_empty = True
        text = static_text.orders_empty


    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_new_orders(ord_empty),
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.MAIN_TREE
