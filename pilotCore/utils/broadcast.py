import re

# from pilotCore.models import Driver
from django_project.settings import TELEGRAM_TOKEN

from telegram import ParseMode, Bot


static_text = 'NEW ORDER RECIVED: \n' \
    '--order id:         {order_id} \n' \
    '--departure time:   {daparture} \n' \
    '--travel direction: {direction} \n' \
    '--seats reserved:   {seats} \n' \
    '--name:             {name}' \
    '{comment}'



def broadcast_new_order(orderObj, driverObj) -> str:
    """broadcasts new orders"""
    """!!! gunicorn NEED REBOOT after changes here !!!"""
    print('---> IN BROADCAST')
    driver_ids = [
        re.sub('[(,)]', '', str(element)) for element in list(driverObj.objects.all().values_list('user_id'))
    ]

    for each in driver_ids:
        chat_id = int(each)
        if ordetObject is '':
            comment = ''
        else:
            comment = '\n--comment' + str(orderObj.comment)

        text = static_text.format(
            order_id = 'no info' if orderObj.order_id is None else orderObj.order_id,
            daparture = 'no info' if orderObj.departure_time is None else orderObj.departure_time,
            direction = 'no info' if orderObj.travel_direction is None else orderObj.travel_direction,
            seats = 'no info' if orderObj.seats is None else orderObj.seats,
            name = 'no info' if orderObj.real_name is None else orderObj.real_name,
            comment = comment
        )


        Bot(TELEGRAM_TOKEN).send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML
        )
    return 'broadcast complete'
