from pilotCore import conversation
# CallbackQueryHandler data:


# Customer main page:
# Back:
TO_CUSTOMER_MAIN_CB = 'TO_CUSTOMER_MAIN_CB'

LIST_ROUTES_CB = 'LIST_ROUTES_CB'
SET_ROUTE_ALERT_CB = 'SET_ROUTE_ALERT_CB'
CUSTOMER_PROPERTIES_CB = 'CUSTOMER_PROPERTIES_CB'


# Available routes page:

# Customer preference page:
# CallBack simmilar to Customer model field names for customer_properties.
CUSTOMER_SET_NAME_CB = 'REAL_NAME_CB'
CUSTOMER_SET_NUMBER_CB = 'MOBILE_NUMBER_CB'
# Redirection patterns:
REPLY_HANDLESR = [
    CUSTOMER_SET_NAME_CB,
    CUSTOMER_SET_NUMBER_CB
]

CONVERSATION_REDIRECT = {
    CUSTOMER_SET_NAME_CB: conversation.CUSTOMER_SET_NAME_CONV,
    CUSTOMER_SET_NUMBER_CB: conversation.CUSTOMER_SET_NUMBER_CONV
}
