from typing import Dict

##### BUTTONS TEXT #####
# driver_main
new_orders = u'\U0001F4B0' + '{alert}' + ' NEW ORDERS'
my_orders = u'\U0001F5D2' + '{alert}' + ' MY ORDERS'
work_time = u'\U000023F3' + ' DEPART TIME'
car_settings = u'\U0001F698' + ' DRIVER PROPERTIES'
direction = u'\U0001F5FA' + ' DIRECTION'

# car_settings
mobile_number = 'Mobile Number'
car_model = 'Car Model'
car_seats = 'Car Seats Number'
car_color = 'Car Color'
car_number = 'Car Number'

# back buttons text:
back_main = u'\U00002B05' + ' Back'
back_my_rides_bt = u'\U00002B05' + ' Back my rides'
back_driver_main = u'\U00002B05' + ' Back'
back_car_settings = u'\U00002B05' + ' Back car setting'


### MESSAGE TEXT ###
request_driver_access_text = 'REQUEST DRIVER ACCESS TEXT'

driver_banned = 'Sorry, You are banned from drivers. \n' \
        'If You disagree - please contact /support'

driver_waiting_approval = 'Your profile waiting approval'

driver_welcome_dialog = 'You can select your car properties to get access faster'

driver_main_text = '<code>      WELCOME DEAR DRIVER</code> \n\n' \
        u'\U0001F6CB <code>Seats.......{seats}</code> \n' \
        u'\U0001F4F1 <code>Tel number..{tel_number}</code>	\n' \
        u'\U0001F698 <code>Car.........{color} {model} {number}</code>' \
        u'{rides_overview}'
        # u'\n<code>    Rides overwview:</code> \n' \

my_rides_overiew = '\n\n' \
        '<code>   {ride_id}</code> \n' \
        '<code>Depart time...{dep_time}</code> \n' \
        '<code>Direction.....{direction}</code> \n' \
        '<code>Seats left....{booked_seats}/{car_seats}</code>'


car_settings_dynamic = '<code>      DRIVER PROPERTIES:</code> \n\n' \
        '<code>Tel number....{mobile}</code> \n' \
        '<code>Car model.....{model}</code> \n' \
        '<code>Car color.....{color}</code> \n' \
        '<code>Car number....{number}</code> \n' \
        '<code>Car seats.....{seats}</code>'

driver_preference_none: Dict[str, str] = {
    'mobile_number': '<code>Enter phone number:</code>',
    'car_model': '<code>Enter car model:</code>',
    'car_seats': '<code>Enter number of seats in the car:</code>',
    'car_color': '<code>Enter car color:</code>',
    'car_number': '<code>Enter car number:</code>',
}

driver_preference_text: Dict[str, str] = {
    'mobile_number': '<code>Your phone number is \n {cb_var} \n To change it reinter number:</code>',
    'car_model': '<code>Your car model is \n {cb_var} \n To change it reinter car model:</code>',
    'car_seats': '<code>Your car number of seats in the car is \n {cb_var} \n To change it reinter car seats number:</code>',
    'car_color': '<code>Your car color is \n {cb_var} \n To change it reinter car color:</code>',
    'car_number': '<code>Your car number is \n {cb_var} \n To change it reinter car number:</code>',
}

## Set handlers text ##
# set_hours_text = '```   Todays working schedule:\n', \
#         '{hours} \n', \
#         'Format: HH:MM-HH:MM   ```'

set_direction_empty = 'Set Your path here'

###### My Rides:
my_rides_bt = u'\U0001F5FA' + ' MY RIDES'
my_rides_new_bt = 'NEW RIDE'
my_rides_del_bt = 'DELETE'
my_rides_edit_bt = 'EDIT'
myrides_empty = 'Your rides is empty for now'
my_rides_time_confirm = 'CONFIRM'

my_rides_text = '``` \n' \
        'Ride id.......{ride_id} \n' \
        'Depart time...{dep_time} \n' \
        'Direction.....{direction} \n' \
        'Seats left....{booked_seats}/{car_seats}' \
        ' ```'
sel_direction_bt = 'Set Direction'

###### Cities set:
del_city = 'DELETE CITY'
conf_direction = 'CONFIRM'
reverse_way = 'ADD REVERSE'

city_Yerevan = 'Yerevan'
city_Ararat = 'Ararat'
city_Ehegnadzor = 'Ehegnadzor'
city_Jermuk = 'Jermuk'
