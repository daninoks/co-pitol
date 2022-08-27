from typing import Dict

##### BUTTONS TEXT #####
# driver_main
pending_orders = u'\U0001F4B0' + ' ORDERS'
work_time = u'\U000023F3' + ' WORK TIME'
car_settings = u'\U0001F698' + ' CAR SETTINGS'
direction = u'\U0001F5FA' + ' DIRECTION'

# car_settings
car_model = 'Car Model'
car_seats = 'Car Seats Number'
car_color = 'Car Color'
car_number = 'Car Number'

# back buttons text:
back_main = u'\U00002B05' + ' Back'
back_driver_main = u'\U00002B05' + ' Back driver main'
back_car_settings = u'\U00002B05' + ' Back car setting'


### MESSAGE TEXT ###
driver_main_text = 'WELCOME DEAR DRIVER\n\n' \
        u'\U0001F4B0 <i>Pending orders</i>...X \n' \
        u'\U000023F3 <i>Work time</i>...........{hours} \n' \
        u'\U0001F5FA <i>Direction</i>.............{direction} \n\n' \
        u'\U0001F698 <i>Car:</i> <b>{seats} seats</b> {color} <b>{model}</b> {number}.'

car_settings_dynamic = 'CAR SETTINGS:\n' \
        'Car model: <b>{model}</b>, \n' \
        'Car color: <b>{color}</b>\n' \
        'Car number: <b>{number}</b>\n' \
        'Car seats: <b>{seats}</b>'


driver_preference_none: Dict[str, str] = {
    'work_hours': 'Enter today working schedule:\n' \
                    'Format: HH:MM-HH:MM',
    'car_model': 'Enter car model:',
    'car_seats': 'Enter number of seats in the car:',
    'car_color': 'Enter car color:',
    'car_number': 'Enter car number:',
}

driver_preference_text: Dict[str, str] = {
    'work_hours': 'Yout toadys work schedule is <b>{cb_var}</b>\n To change it reinter work schedule:\n' \
                    'Format: HH:MM-HH:MM',
    'car_model': 'Your car model is\n <b>{cb_var}</b>\n To change it reinter car model:',
    'car_seats': 'Your car number of seats in the car is\n <b>{cb_var}</b>\n To change it reinter car seats number:',
    'car_color': 'Your car color is\n <b>{cb_var}</b>\n To change it reinter car color:',
    'car_number': 'Your car number is\n <b>{cb_var}</b>\n To change it reinter car number:',
}


######
del_city = 'DELETE CITY'
conf_direction = 'CONFIRM'
reverse_way = 'ADD REVERSE'

city_Yerevan = 'Yerevan'
city_Ararat = 'Ararat'
city_Ehegnadzor = 'Ehegnadzor'
city_Jermuk = 'Jermuk'
