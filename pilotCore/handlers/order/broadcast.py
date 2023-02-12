# import re

# from telegram import ParseMode, Bot

# from django_project.settings import TELEGRAM_TOKEN
# from pilotCore import conversation
# from pilotCore.handlers.order import (
#     static_text, keyboards
# )


# def broadcast_new_order(orderObj, driverObj, UserObj) -> int:
#     """broadcasts new orders"""
#     """!!! gunicorn NEED REBOOT after changes here !!!"""
#     #print('---> IN BROADCAST')
#     driver_ids = [
#         re.sub('[(,)]', '', str(element)) for element in list(driverObj.objects.all().values_list('user_id'))
#     ]

#     for each in driver_ids:
#         chat_id = int(each)

#         text = static_text.broadcast_text.format(
#             order_id = (
#                 'no info' if orderObj.order_id is None
#                 else orderObj.order_id
#             ),
#             daparture = (
#                 'no info' if orderObj.departure_time is None
#                 else orderObj.departure_time
#             ),
#             direction = (
#                 'no info' if orderObj.travel_direction is None
#                 else orderObj.travel_direction
#             ),
#             seats = (
#                 'no info' if orderObj.seats is None
#                 else orderObj.seats
#             ),
#             name = (
#                 'no info' if orderObj.real_name is None
#                 else orderObj.real_name)
#             ,
#             comment = (
#                 '' if orderObj.comment == ''
#                 else '\n--comment:\n' + str(orderObj.comment)
#             ),
#             pointed = ''
#         )

#         #print('test')

#         du = UserObj.get_user_by_username_or_user_id(chat_id)
#         mess_id = du.last_msg_id
#         # mess_id = UserObj.objects.filter(user_id=int(chat_id)).first()
#         # #print(du)

#         Bot(TELEGRAM_TOKEN).deleteMessage(
#             chat_id=chat_id,
#             message_id=mess_id,
#             timeout=None
#         )
#         Bot(TELEGRAM_TOKEN).send_message(
#             text=text,
#             chat_id=chat_id,
#             reply_markup=keyboards.make_keyboard_broadcast(),
#             parse_mode=ParseMode.HTML
#         )
#     return conversation.MAIN_TREE
