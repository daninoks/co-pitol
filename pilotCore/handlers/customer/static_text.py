from typing import Dict

# Empty fields:
customer_empty_fields = "<code>Please fill this field</code>"

# Customer aproval dialog:
customer_welcome_dialog_tx = (
    "<code>You can pass your properties to get access faster</code>"
)
customer_waiting_aproval_tx = "<code>Your profile waiting approval</code>"
customer_banned_tx = (
    "<code>Sorry, You are banned from this bot.</code> \n"
    "<code>If You disagree - please contact</code> /support"
)

# Customer main page:
customer_main_tx = (
    "<code>Hello customer</code> \n" "<code>Customer overview here</code>"
)

list_routes_bt = "available routes"
set_route_alert_bt = "set route alert"
customer_properties_bt = "customer properties"

customer_main_ride_booked_tx = (
    "\n"
    "<code>       BOOKED RIDE:</code> \n"
    "<code>Ride id............{ride_id}</code> \n"
    "<code>Depart time........{dep_time}</code> \n"
    "<code>Direction..........{direction}</code> \n"
    "<code>Seats booked.......{seats_booked}</code>"
)


# Customer list routes page:
routes_select_bt = "Select"


# Customer properties page:
customer_properties_tx = (
    "<code>Name...............{name}</code> \n" "<code>Mob.Number.........{tel}</code>"
)


customer_set_name_bt = "set name"
customer_set_number_bt = "set nubmer"

customer_properties_empty_dt: Dict[str, str] = {
    "real_name": "<code>Please enter Your real name</code>",
    "mobile_number": "<code>Please enter Your telephone number</code>",
}
customer_properties_set_dt: Dict[str, str] = {
    "real_name": "Current name: {cb_var} \n To change it send me new name.",
    "mobile_number": "Current number: {cb_var} \n To change it send me new number.",
}


# Select seats:
customer_select_seats_confirm_bt = "Confirm"
customer_ride_confirm_bt = "Confirm"

customer_select_seats_tx = (
    "\n"
    "<code>Ride id............{ride_id}</code> \n"
    "<code>Depart time........{dep_time}</code> \n"
    "<code>Direction..........{direction}</code> \n"
    "<code>Seats sel/avail....{sel_seats}/{avail_seats}</code>"
    "<code>\n\n {warning_mess}</code>"
)

select_seats_min_warning_mess = "<code>You cant select less then 1 seats</code>"
select_seats_max_warning_mess = (
    "<code>You cant select more then {car_seats} seats</code>"
)
select_seats_warning_mess = (
    "<code>!If you confirm ride, you can not cancel it in future!</code>"
)
