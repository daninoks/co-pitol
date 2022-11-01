"""
    Telegram event handlers
"""
import sys
import logging

import telegram.error

from typing import Dict

from telegram import (
    Bot, Update, BotCommand,
    CallbackQuery,
)
from telegram.ext import (
    Updater, Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler, RegexHandler,
    ConversationHandler, Handler,
)

from django_project.settings import TELEGRAM_TOKEN, DEBUG
from django_project.celery import app  # event processing in async mode

from pilotCore.handlers.utils import error
from pilotCore import conversation
from pilotCore.handlers.welcome import handlers as welcome_handlers
from pilotCore.handlers.welcome import manage_data as welcome_data
from pilotCore.handlers.driver import handlers as driver_handlers
from pilotCore.handlers.driver import manage_data as driver_data
from pilotCore.handlers.customer import handlers as customer_handlers
from pilotCore.handlers.customer import manage_data as customer_data


from pilotCore.handlers.order import handlers as order_handlers
from pilotCore.handlers.order import manage_data as order_data
from pilotCore.handlers.operator import handlers as operator_handlers
from pilotCore.handlers.operator import manage_data as operator_data

from pilotCore.handlers.goto import manage_data as goto_data

# TELEGRAM_TOKEN = TELEGRAM_TOKEN


def make_conversation_handler():
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", welcome_handlers.command_start),
            CommandHandler("reg_operator", operator_handlers.reg_operator),
            # CommandHandler("driver", driver_handlers.driver_main),
            CallbackQueryHandler(
                order_handlers.new_orders_menu,
                pattern=format(
                    f'^{order_data.GO_TO_NEW_ORDERS}$'
                )
            )
        ],
        states={
            conversation.MAIN_TREE: [
                CallbackQueryHandler(
                    welcome_handlers.start_over,
                    pattern=format(
                        f'^{goto_data.GO_START_OVER_CB}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.driver_main,
                    pattern=format(
                        f'^{welcome_data.DRIVER_BUTTON}$|'
                        f'^{goto_data.GO_DRIVER_MAIN_CB}$'
                    )
                ),
                CallbackQueryHandler(
                    order_handlers.new_orders_menu,
                    pattern=format(
                        f'^{driver_data.NEW_ORDERS_BUTTON}$|'
                        f'^{order_data.NOM_PREV_ORDER}$|'
                        f'{order_data.NOM_DYNAMIC_CB_ORD_PATT}'
                        f'^{order_data.NOM_NEXT_ORDER}$|'
                        f'^{order_data.NOM_ACCEPT_ORDER_BUTTON}$|'
                        f'^{order_data.NOM_DECLINE_ORDER_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    order_handlers.my_orders_menu,
                    pattern=format(
                        f'^{driver_data.MY_ORDERS_BUTTON}$|'
                        f'^{order_data.MOM_PREV_ORDER}$|'
                        f'{order_data.MOM_DYNAMIC_CB_ORD_PATT}'
                        f'^{order_data.MOM_NEXT_ORDER}$|'
                        f'^{order_data.MOM_DECLINE_ORDER_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.my_rides,
                    pattern=format(
                        f'^{driver_data.MY_RIDES_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{driver_data.CAR_SETTINGS_BUTTON}$|'
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.driver_preference,
                    pattern=format(
                        f'^{driver_data.CAR_MODEL_BUTTON}$|'
                        f'^{driver_data.CAR_SEATS_BUTTON}$|'
                        f'^{driver_data.CAR_COLOR_BUTTON}$|'
                        f'^{driver_data.CAR_NUMBER_BUTTON}$|'
                        f'^{driver_data.MOBILE_NUMBER_BUTTON}$'
                    )
                ),
                # Customer converstions:
                CallbackQueryHandler(
                    customer_handlers.customer_main,
                    pattern=format(
                        f'^{welcome_data.CUSTOMER_BUTTON}$|'
                        f'^{goto_data.GO_CUSTOMER_MAIN_CB}$'
                    )
                ),
                CallbackQueryHandler(
                    customer_handlers.customer_properties,
                    pattern=format(
                        f'^{customer_data.CUSTOMER_PROPERTIES_CB}$|'
                        f'^{goto_data.GO_CUSTOMER_PROPERTIES_CB}$|'
                        f'^{customer_data.CUSTOMER_SET_NAME_CB}$|'
                        f'^{customer_data.CUSTOMER_SET_NUMBER_CB}$'
                    )
                ),

                # Catch unnessesary messages from user:
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.delete_missclicked_messages
                ),
            ],
            # Driver set model:
            conversation.MODEL_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.set_model
                ),
            ],
            # Driver set seats:
            conversation.SEATS_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.set_seats
                ),
            ],
            # Driver set color:
            conversation.COLOR_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.set_color
                ),
            ],
            # Driver set cra number:
            conversation.NUMBER_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.set_number
                ),
            ],
            # Driver set mobile number:
            conversation.MOBILE_NUMBER_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{goto_data.GO_CAR_SETTING_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.set_mobile_number
                ),
            ],
            # Driver directions number:
            conversation.RIDES_CONV: [
                CallbackQueryHandler(
                    driver_handlers.driver_main,
                    pattern=format(
                        f'^{goto_data.GO_DRIVER_MAIN_CB}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.my_rides,
                    pattern=format(
                        f'^{driver_data.MY_RIDES_BUTTON}$|'
                        f'{driver_data.MR_DYNAMIC_CB_RIDE_PATT}'
                        f'^{driver_data.MR_PREV_RIDE}$|'
                        f'^{driver_data.MR_NEXT_RIDE}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.my_rides_edit,
                    pattern=format(
                        f'^{driver_data.MY_RIDES_NEW_BUTTON}$|'
                        f'^{driver_data.MY_RIDES_EDIT_BUTTON}$|'
                        f'^{driver_data.MY_RIDES_DEL_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.set_direction,
                    pattern=format(
                        f'^{driver_data.SEL_DIRECTION_BUTTON}$|'
                        f'^{driver_data.CITIES_PATTERN}$|'
                        f'^{driver_data.DELETE_CITY_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), driver_handlers.my_rides_time
                ),
            ],
            # Customer set real name:
            conversation.CUSTOMER_SET_NAME_CONV: [
                CallbackQueryHandler(
                    customer_handlers.customer_properties,
                    pattern=format(
                        f'^{goto_data.GO_CUSTOMER_PROPERTIES_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), customer_handlers.set_customer_name
                ),
            ],
            # Customer set mobile number:
            conversation.CUSTOMER_SET_NUMBER_CONV: [
                CallbackQueryHandler(
                    customer_handlers.customer_properties,
                    pattern=format(
                        f'^{goto_data.GO_CUSTOMER_PROPERTIES_CB}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/).*$'), customer_handlers.set_customer_number
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', welcome_handlers.command_start),
            CommandHandler("reg_operator", operator_handlers.reg_operator),
            # CommandHandler("driver", driver_handlers.driver_main),
            # CallbackQueryHandler(
            #     order_handlers.new_orders_menu,
            #     pattern=format(
            #         f'^{order_data.GO_TO_NEW_ORDERS}$'
            #     )
            # )
        ],
        per_message=False,
    )

    return conv_handler


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram.
    """
    # start Commands:
    # dp.add_handler(CommandHandler("start", welcome_handlers.command_start))
    # dp.add_handler(CommandHandler("driver", driver_handlers.driver_main))

    conv_handler = make_conversation_handler()
    dp.add_handler(conv_handler)

    return dp


def run_pooling():
    """
    Get webhook info:
        https://api.telegram.org/bot{my_bot_token}/getWebhookInfo
    Set/Del webhook:
        https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
        https://api.telegram.org/bot5126359997:AAGh1sJhPxgunORtB9JjObbYob3R1u56xWw/setWebhook?url=https://194-67-74-48.cloudvps.regruhosting.ru/webhook/

        https://api.telegram.org/bot{my_bot_token}/deleteWebhook?url={url_to_send_updates_to}
        https://api.telegram.org/bot5126359997:AAGh1sJhPxgunORtB9JjObbYob3R1u56xWw/deleteWebhook?url=https://194-67-74-48.cloudvps.regruhosting.ru/webhook/
    """

    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN)
try:
    TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
    logging.error(f"Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
    langs_with_commands: Dict[str, Dict[str, str]] = {
        'en': {
            'start': 'Start bot 🚀',
            'admin': 'Show admin info ℹ️',
        },
        'ru': {
            'start': 'Запустить бота 🚀',
            'admin': 'Показать информацию для админов ℹ️',
        }
    }

    bot_instance.delete_my_commands()
    for language_code in langs_with_commands:
        bot_instance.set_my_commands(
            language_code=language_code,
            commands=[
                BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
            ]
        )


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
# set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))

# if __name__ == '__main__':
#     run_pooling()
