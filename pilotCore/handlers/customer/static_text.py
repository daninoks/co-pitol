
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


# Available routes page:

# Customer properties page:
customer_properties_tx = 'Name -- {name} \n' \
        'Mob.Number -- {tel}'

customer_set_name_bt = 'set name'
customer_set_number_bt = 'set nubmer'

customer_properties_empty_dt: Dict[str, str] ={
        'real_name': 'Please enter Your real name'
        'mobile_number': 'Please enter Your telephone number'
}
customer_properties_set_dt: Dict[str, str] = {
        'real_name': 'Please enter Your real name: \n Current name: {cb_var}'
        'mobile_number': 'Please enter Your telephone number: \n Current number: {cb_var}'
}
