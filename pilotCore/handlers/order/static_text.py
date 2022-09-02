from typing import Dict

##### BUTTONS TEXT #####
decline_order = u'\U0000274C' + ' CANCEL'
accept_order = u'\U00002714' + ' ACCEPT'

go_to_new_orders = 'CHECK ORDERS'


### MESSAGE TEXT ###
broadcast_text = '```     NEW ORDER RECIVED: \n' \
    u'\U0001F194  order id:         {order_id} \n' \
    u'\U000023F1  departure time:   {daparture} \n' \
    u'\U0001F5FA  travel direction: {direction} \n' \
    u'\U0001F6CB  seats reserved:   {seats} \n' \
    u'\U0001F464  name:             {name}' \
    u'{comment}```'


new_orders_body = '```     NEW ORDER RECIVED: \n' \
    u'\U0001F194  order id:...........{order_id} \n' \
    u'\U000023F1  departure time:.....{daparture} \n' \
    u'\U0001F5FA  travel direction:...{direction} \n' \
    u'\U0001F6CB  seats reserved:.....{seats} \n' \
    u'\U0001F464  name:...............{name}' \
    '{comment} \n\n {pointed}```'

orders_empty = '``` NO AVAILABLE ORDERDS FOR NOW```'
