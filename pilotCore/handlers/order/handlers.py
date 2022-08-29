import re

from telegram import (
    ParseMode, Update, ForceReply, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup,
    Bot, ForceReply
)
from telegram.ext import CallbackContext

from pilotCore import conversation
from pilotCore.models import Order, Driver, DriverUtils
from pilotCore.handlers.order import static_text, manage_data, keyboards



def update_order_list(update) -> list:
    new_orders_open = list(Order.objects.filter(status=Order.ORD_OPEN).values(
        'order_id', 'departure_time', 'travel_direction',
        'seats', 'real_name', 'comment', 'status', 'pointed'
    ))
    new_orders_pendig = list(
        Order.objects.filter(
            status=Order.ORD_PENDING,
            pointed=update.callback_query.message.chat.id,
        ).values(
            'order_id', 'departure_time', 'travel_direction',
            'seats', 'real_name', 'comment', 'status', 'pointed'
    ))
    if new_orders_pendig:
        new_orders_open.extend(new_orders_pendig)
    return new_orders_open



def new_orders_menu(update: Update, context: CallbackContext) -> int:
    """Handle NEW_ORDERS_BUTTON Query command"""
    call_back = update.callback_query.data
    print(call_back)

    new_orders = update_order_list(update)

    if new_orders:
        ord_empty = False
        last_element = 0 if len(new_orders) == 0 else len(new_orders) - 1   # cant be 0 by if(?)
        no_num = DriverUtils.set_new_orders_num(update, context, last_element)

        du, _ = DriverUtils.get_or_create_user(update, context)
        no_page = du.new_orders_page

        if call_back == manage_data.NEXT_ORDER:
            no_page = DriverUtils.set_new_orders_page(update, context, -2)
        if call_back == manage_data.PREV_ORDER:
            no_page = DriverUtils.set_new_orders_page(update, context, -1)
        if call_back in manage_data.DYNAMIC_CB_NEW_ORD:
            print(re.sub('cb:', '', call_back))
            no_page = DriverUtils.set_new_orders_page(
                update,
                context,
                int(re.sub('cb:', '', call_back))
            )

        # keyboard pages:
        current_page_marker = u'\U000025CF'
        page_selected = no_page
        pages_number = no_num + 1
        print('page_selected ' + str(page_selected))
        print('pages_number ' + str(pages_number))
        # pages_list = list(range(0, last_element + 1))
        max_listing_num = 5 if pages_number >= 5 else pages_number

        if pages_number > 5:
            if page_selected <= 3:
                pages_layout = list(range(0, 5))
                ind = pages_layout.index(page_selected)
                pages_layout[ind] = current_page_marker
            elif page_selected >= pages_number - 3:
                pages_layout = list(range(pages_number - 5, pages_number))
                ind = pages_layout.index(page_selected)
                pages_layout[ind] = current_page_marker
            else:
                pages_layout = list(range(page_selected - 2, page_selected + 3))
                ind = pages_layout.index(page_selected)
                pages_layout[ind] = current_page_marker
        else:
            pages_layout = list(range(0, pages_number))
            pages_layout[page_selected] = current_page_marker

        # current page object:
        orderObj = new_orders[no_page]

        if call_back == manage_data.ACCEPT_ORDER_BUTTON:
            Order.link_order(update, context, orderObj.get('order_id'))
            new_orders = update_order_list(update)
            orderObj = new_orders[no_page]

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
                else u'\n\U0001F4DC  comment: ' + str(orderObj.get('comment'))
            ),
            pointed = (
                u'\U0000203C  YOU ACCEPT THIS ORDER  \U0000203C' if orderObj.get('pointed') == update.callback_query.message.chat.id
                else ''
            ),
            seats = orderObj.get('seats')
        )
    else:
        ord_empty = True
        pages_layout = None
        text = static_text.orders_empty


    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_new_orders(ord_empty, pages_layout),
        parse_mode=ParseMode.MARKDOWN
    )
    return conversation.MAIN_TREE
