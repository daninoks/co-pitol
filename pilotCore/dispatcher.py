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


TELEGRAM_TOKEN = TELEGRAM_TOKEN


def make_conversation_handler():
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", welcome_handlers.command_start),
            # CommandHandler("driver", driver_handlers.driver_main),
        ],
        states={
            conversation.MAIN_TREE: [
                CallbackQueryHandler(
                    welcome_handlers.test,
                    pattern=format(
                        f'^{welcome_data.TEST_BUTTON}$|'
                    )
                ),
                CallbackQueryHandler(
                    welcome_handlers.start_over,
                    pattern=format(
                        f'^{driver_data.BACK_MAIN_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.driver_main,
                    pattern=format(
                        f'^{welcome_data.DRIVER_BUTTON}$|'
                        f'^{driver_data.BACK_DRIVER_MAIN_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{driver_data.CAR_SETTINGS_BUTTON}$|'
                        f'^{driver_data.BACK_CAR_SETTING_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.driver_preference,
                    pattern=format(
                        f'^{driver_data.WORK_HOURS_BUTTON}$|'
                        f'^{driver_data.CAR_MODEL_BUTTON}$|'
                        f'^{driver_data.CAR_SEATS_BUTTON}$|'
                        f'^{driver_data.CAR_COLOR_BUTTON}$|'
                        f'^{driver_data.CAR_NUMBER_BUTTON}$'
                    )
                ),
                CallbackQueryHandler(
                    driver_handlers.set_direction,
                    pattern=format(
                        f'^{driver_data.DIRECTION_BUTTON}$|'
                        f'^{driver_data.DELETE_CITY_BUTTON}$|'
                        f'{driver_data.CITIES_PATTERN}'
                    )
                ),
                # Catch unnessesary messages from user:
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.delete_missclicked_messages
                ),
            ],
            conversation.MODEL_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{driver_data.BACK_CAR_SETTING_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.set_model
                ),
            ],
            conversation.SEATS_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{driver_data.BACK_CAR_SETTING_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.set_seats
                ),
            ],
            conversation.COLOR_CONV: [
                CallbackQueryHandler(
                    driver_handlers.car_settings,
                    pattern=format(
                        f'^{driver_data.BACK_CAR_SETTING_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.set_color
                ),
            ],
            conversation.NUMBER_CONV: [
                CallbackQueryHandler(
                    driver_handlers.driver_main,
                    pattern=format(
                        f'^{driver_data.BACK_DRIVER_MAIN_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.set_number
                ),
            ],
            conversation.HOURS_CONV: [
                CallbackQueryHandler(
                    driver_handlers.driver_main,
                    pattern=format(
                        f'^{driver_data.BACK_DRIVER_MAIN_BUTTON}$'
                    )
                ),
                MessageHandler(
                    Filters.regex('^(?!\/start).*$'), driver_handlers.set_hours
                ),
            ],
        },
        fallbacks=[
            CommandHandler('start', welcome_handlers.command_start),
            # CommandHandler("driver", driver_handlers.driver_main),
        ],
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
            'start': 'Start django bot 🚀',
            'admin': 'Show admin info ℹ️',
        },
        'ru': {
            'start': 'Запустить django бота 🚀',
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
