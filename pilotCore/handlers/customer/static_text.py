from typing import Dict

# Empty fields:
customer_empty_fields = 'Please fill this field'

# Customer aproval dialog:
customer_welcome_dialog_tx = 'You can pass your properties to get access faster'
customer_waiting_aproval_tx = 'Your profile waiting approval'
customer_banned_tx = 'Sorry, You are banned from this bot. \n' \
        'If You disagree - please contact /support'
# Customer main page:
customer_main_tx = 'Hello customer \n' \
        'Customer overview here'

list_routes_bt = 'available routes'
set_route_alert_bt = 'set route alert'
customer_properties_bt = 'customer properties'

customer_main_ride_booked_tx = '``` \n' \
        '       BOOKED RIDE: \n' \
        'Ride id............{ride_id} \n' \
        'Depart time........{dep_time} \n' \
        'Direction..........{direction} \n' \
        'Seats booked.......{seats_booked}' \
        ' ```'


# Customer list routes page:
routes_select_bt = 'Select'




# Customer properties page:
customer_properties_tx = 'Name -- {name} \n' \
        'Mob.Number -- {tel}'

customer_set_name_bt = 'set name'
customer_set_number_bt = 'set nubmer'

customer_properties_empty_dt: Dict[str, str] = {
        'real_name': 'Please enter Your real name',
        'mobile_number': 'Please enter Your telephone number'
}
customer_properties_set_dt: Dict[str, str] = {
        'real_name': 'Current name: {cb_var} \n To change it send me new name.',
        'mobile_number': 'Current number: {cb_var} \n To change it send me new number.'
}




# Select seats:
customer_select_seats_confirm_bt = 'Confirm'
customer_ride_confirm_bt = 'Confirm'

customer_select_seats_tx = '``` \n' \
        'Ride id............{ride_id} \n' \
        'Depart time........{dep_time} \n' \
        'Direction..........{direction} \n' \
        'Seats sel/avail....{sel_seats}/{avail_seats}' \
        '\n\n {warning_mess}' \
        ' ```'

select_seats_min_warning_mess = 'You cant select less then 1 seats'
select_seats_max_warning_mess = 'You cant select more then {car_seats} seats'
select_seats_warning_mess = '!If you confirm ride, you can not cancel it in future!'

