from pilotCore import conversation
from pilotCore.handlers.order import static_text




# CallbackQueryHandler data:
DECLINE_ORDER_BUTTON = 'DCLN_RDR_BTTN'
ACCEPT_ORDER_BUTTON = 'CCPT_RDR_BTTN'

PREV_ORDER = 'PRV_RDR'
NEXT_ORDER = 'NXT_RDR'

dynamic_callback_patt = [f'^cb:{i}$|' for i in range(100)]
DYNAMIC_CB_NEW_ORD_PATT = ''.join(dynamic_callback_patt)
DYNAMIC_CB_NEW_ORD = [f'cb:{i}' for i in range(100)]
