import logging
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from pilotCore import conversation

from pilotCore.handlers.welcome import (
        keyboards as welcome_keyboards, 
        manage_data as welcome_data, 
        static_text as welcome_text
)
from pilotCore.models import User




def command_start(update: Update, context: CallbackContext) -> int:
    """Handle start command"""
    logging.debug(msg='Comand start handled \n' + str(update))
    
    User.set_last_msg_id(update, context)

    text = welcome_text.command_start_text
    update.message.reply_text(
        text=text,
        reply_markup=welcome_keyboards.make_keyboard_start_command()
    )
    return conversation.MAIN_TREE

def start_over(update: Update, context: CallbackContext) -> int:
    """Handle all back moves to start page"""
    logging.debug(msg='Comand start_over handled \n' + str(update))

    text = welcome_text.command_start_text
    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=welcome_keyboards.make_keyboard_start_command(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE
