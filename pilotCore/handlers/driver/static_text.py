from typing import Dict

##### BUTTONS TEXT #####
# driver_main
new_orders = "\U0001F4B0" + "{alert}" + " NEW ORDERS"
my_orders = "\U0001F5D2" + "{alert}" + " MY ORDERS"
work_time = "\U000023F3" + " DEPART TIME"
car_settings = "\U0001F698" + " DRIVER PROPERTIES"
direction = "\U0001F5FA" + " DIRECTION"

# car_settings
mobile_number = "Mobile Number"
car_model = "Car Model"
car_seats = "Car Seats Number"
car_color = "Car Color"
car_number = "Car Number"


### MESSAGE TEXT ###
request_driver_access_text = "<code>REQUEST DRIVER ACCESS TEXT</code>"

driver_banned = (
    "<code>Sorry, You are banned from drivers.</code> \n"
    "<code>If You disagree - please contact</code> /support"
)


driver_waiting_approval = "<code>Your profile waiting approval</code>"

driver_welcome_dialog = (
    "<code>You can select your car properties to get access faster</code>"
)

driver_main_text = (
    "<code>      WELCOME DEAR DRIVER</code> \n\n"
    "\U0001F6CB <code>Seats.......{seats}</code> \n"
    "\U0001F4F1 <code>Tel number..{tel_number}</code> \n"
    "\U0001F698 <code>Car.........{color} {model} {number}</code>"
    "{rides_overview}"
)


my_rides_overiew = (
    "\n\n"
    "<code>   {ride_id}</code> \n"
    "<code>Depart time.......{dep_time}</code> \n"
    "<code>Direction.........{direction}</code> \n"
    "<code>Seats reserved....{booked_seats}/{car_seats}</code>"
)


car_settings_dynamic = (
    "<code>      DRIVER PROPERTIES:</code> \n"
    "<code>Tel number....{mobile}</code> \n"
    "<code>Car model.....{model}</code> \n"
    "<code>Car color.....{color}</code> \n"
    "<code>Car number....{number}</code> \n"
    "<code>Car seats.....{seats}</code> \n"
)


driver_preference_none: Dict[str, str] = {
    "mobile_number": "<code>Enter phone number:</code>",
    "car_model": "<code>Enter car model:</code>",
    "car_seats": "<code>Enter number of seats in the car:</code>",
    "car_color": "<code>Enter car color:</code>",
    "car_number": "<code>Enter car number:</code>",
}

driver_preference_text: Dict[str, str] = {
    "mobile_number": (
        "<code>Your phone number is</code> \n {cb_var} \n"
        "<code>To change it reinter number: +374(44)123456</code>"
    ),
    "car_model": "<code>Your car model is \n {cb_var} \n To change it reinter car model:</code>",
    "car_seats": "<code>Your car number of seats in the car is \n {cb_var} \n To change it reinter car seats number:</code>",
    "car_color": "<code>Your car color is \n {cb_var} \n To change it reinter car color:</code>",
    "car_number": "<code>Your car number is \n {cb_var} \n To change it reinter car number:</code>",
}


set_direction_empty = "<code>Set Your path here</code>"

###### My Rides:
my_rides_bt = "\U0001F5FA" + " MY RIDES"
my_rides_new_bt = "NEW RIDE"
my_rides_del_bt = "DELETE"
my_rides_edit_bt = "EDIT"
myrides_empty = "<code>Your rides is empty for now</code>"
my_rides_time_confirm = "CONFIRM"

my_rides_text = (
    "\n"
    "<code>Ride id.......{ride_id}</code> \n"
    "<code>Depart time...{dep_time}</code> \n"
    "<code>Direction.....{direction}</code> \n"
    "<code>Seats reserved....{booked_seats}/{car_seats}</code>"
)


sel_direction_bt = "Set Direction"

###### Cities set:
del_city = "DELETE CITY"
conf_direction = "CONFIRM"
reverse_way = "ADD REVERSE"

city_Yerevan = "Yerevan"
city_Ararat = "Ararat"
city_Ehegnadzor = "Ehegnadzor"
city_Jermuk = "Jermuk"
