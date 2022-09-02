from typing import Dict

##### BUTTONS TEXT #####
# driver_main
new_orders = u'\U0001F4B0' + '{alert}' + ' NEW ORDERS'
my_orders = u'\U0001F5D2' + '{alert}' + ' MY ORDERS'
work_time = u'\U000023F3' + ' DEPART TIME'
car_settings = u'\U0001F698' + ' DRIVER PROPERTIES'
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
driver_main_text = '<code>      WELCOME DEAR DRIVER</code> \n\n' \
        u'\U0001F4B0 <code>Orders......X</code> \n' \
        u'\U000023F3 <code>Work time...{hours}</code>\n' \
        u'\U0001F5FA <code>Direction...{direction}</code> \n' \
        u'\U0001F6CB <code>Seats.......{seats}</code> \n' \
        u'\U0001F698 <code>Car.........{color} {model} {number}</code>'

car_settings_dynamic = '<code>      DRIVER PROPERTIES:</code> \n\n' \
        '<code>Tel number....{mobile}</code> \n' \
        '<code>Car model.....{model}</code> \n' \
        '<code>Car color.....{color}</code> \n' \
        '<code>Car number....{number}</code> \n' \
        '<code>Car seats.....{seats}</code>'


driver_preference_none: Dict[str, str] = {
    'work_hours': 'Enter todays working schedule: \n Format: HH:MM-HH:MM',
    'car_model': 'Enter car model:',
    'car_seats': 'Enter number of seats in the car:',
    'car_color': 'Enter car color:',
    'car_number': 'Enter car number:',
}

driver_preference_text: Dict[str, str] = {
    'work_hours': 'Yout toadys work schedule is <b>{cb_var}</b>\n To change it reinter work schedule: \n Format: HH:MM-HH:MM',
    'car_model': 'Your car model is\n <b>{cb_var}</b>\n To change it reinter car model:',
    'car_seats': 'Your car number of seats in the car is\n <b>{cb_var}</b>\n To change it reinter car seats number:',
    'car_color': 'Your car color is\n <b>{cb_var}</b>\n To change it reinter car color:',
    'car_number': 'Your car number is\n <b>{cb_var}</b>\n To change it reinter car number:',
}

## Set handlers text ##
set_hours_text = '```   Todays working schedule:\n', \
    '{hours} \n', \
    'Format: HH:MM-HH:MM   ```'

set_direction_empty = 'Set Your path here'




######
del_city = 'DELETE CITY'
conf_direction = 'CONFIRM'
reverse_way = 'ADD REVERSE'

city_Yerevan = 'Yerevan'
city_Ararat = 'Ararat'
city_Ehegnadzor = 'Ehegnadzor'
city_Jermuk = 'Jermuk'
