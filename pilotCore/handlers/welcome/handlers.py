from telegram import ParseMode, Update, ForceReply, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pilotCore import conversation

from pilotCore.handlers.welcome import keyboards, manage_data, static_text
from pilotCore.models import User, PrevMess


### tests needs ###
from pilotCore.utils import broadcast

def command_start(update: Update, context: CallbackContext) -> int:
    """Handle start command"""
    cu = PrevMess.reset_counter(update, context)    # reset needed only when commands handled

    text = static_text.command_start_text
    print('---> Comand start handled')
    update.message.reply_text(
        text=text,
        reply_markup=keyboards.make_keyboard_start_command()
    )
    return conversation.MAIN_TREE

def start_over(update: Update, context: CallbackContext) -> int:
    """Handle all back moves to main page"""

    text = static_text.command_start_text
    print('---> Start over handled')
    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_start_command(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE

def test(update: Update, context: CallbackContext) -> int:
    """For test needs"""

    text = broadcast.broadcast_new_order()

    print('IN TEST HANDLER')

    context.bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat.id,
        message_id=update.callback_query.message.message_id,
        reply_markup=keyboards.make_keyboard_start_command(),
        parse_mode=ParseMode.HTML
    )
    return conversation.MAIN_TREE
