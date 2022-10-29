from pilotCore import conversation
from pilotCore.handlers.driver import static_text
# CallbackQueryHandler data:

# driver_main:
NEW_ORDERS_BUTTON = 'NW_ORD_BTTN'
MY_ORDERS_BUTTON = 'M_ORD_BTTN'
CAR_SETTINGS_BUTTON = 'CR_STTNGS_BTTN'
# DIRECTION_BUTTON = 'DIRECTION_BTTN'

# driver_preference:
MOBILE_NUMBER_BUTTON = 'MOBILE_NUMBER_BTTN'
CAR_MODEL_BUTTON = 'CAR_MODEL_BTTN'
CAR_SEATS_BUTTON = 'CAR_SEATS_BTTN'
CAR_COLOR_BUTTON = 'CAR_COLOR_BTTN'
CAR_NUMBER_BUTTON = 'CAR_NUMBER_BTTN'

# Driver preference redirection patterns:
REPLY_HANDLESR = [
    MOBILE_NUMBER_BUTTON,
    CAR_MODEL_BUTTON,
    CAR_SEATS_BUTTON,
    CAR_COLOR_BUTTON,
    CAR_NUMBER_BUTTON
]

CONVERSATION_REDIRECT = {
    MOBILE_NUMBER_BUTTON: conversation.MOBILE_NUMBER_CONV,
    CAR_MODEL_BUTTON: conversation.MODEL_CONV,
    CAR_SEATS_BUTTON: conversation.SEATS_CONV,
    CAR_COLOR_BUTTON: conversation.COLOR_CONV,
    CAR_NUMBER_BUTTON: conversation.NUMBER_CONV
}

SEL_DIRECTION_BUTTON = 'SL_DRCTN_BTTN'

####### My Rides:
##### Dynamic keyboard scroll:
MR_PREV_RIDE = 'MR_PRV_RDR'
MR_NEXT_RIDE = 'MR_NXT_RDR'

MR_CB_PREFIX = 'mr_cb'
mr_dynamic_callback_patt = [f'^{MR_CB_PREFIX}:{i}$|' for i in range(25)]

MR_DYNAMIC_CB_RIDE_PATT = ''.join(mr_dynamic_callback_patt)
MR_DYNAMIC_CB_RIDE = [f'{MR_CB_PREFIX}:{i}' for i in range(25)]
#####
MY_RIDES_BUTTON = 'MY_RIDES_BTTN'
MY_RIDES_NEW_BUTTON = 'MY_RIDES_NEW_BTTN'

MY_RIDES_DEL_BUTTON = 'MY_RIDES_DEL_BTTN'
MY_RIDES_EDIT_BUTTON = 'MY_RIDES_EDIT_BTTN'

MY_RIDES_TIME_CONFIRM = 'MY_RIDES_TIME_CONFIRM_BTTN'


####### Cities
DELETE_CITY_BUTTON = 'DLT_CT_BTTN'

CITY_YEREVAN_BUTTON = 'CT_RVN_BTTN'
CITY_ARARAT_BUTTON = 'CT_RRT_BTTN'
CITY_EHEGNADZOR_BUTTON = 'CT_HGNDZR_BTTN'
CITY_JERMUK_BUTTON = 'CT_JRMK_BTTN'


CITIES_CALLBACK = {
    CITY_YEREVAN_BUTTON: static_text.city_Yerevan,
    CITY_ARARAT_BUTTON: static_text.city_Ararat,
    CITY_EHEGNADZOR_BUTTON: static_text.city_Ehegnadzor,
    CITY_JERMUK_BUTTON: static_text.city_Jermuk
}
CITIES_PATTERN = f'^{CITY_YEREVAN_BUTTON}$|' \
                    f'^{CITY_ARARAT_BUTTON}$|' \
                    f'^{CITY_EHEGNADZOR_BUTTON}$|' \
                    f'^{CITY_JERMUK_BUTTON}$'
