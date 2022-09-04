import time

from telegram import ParseMode, Update, ForceReply, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pilotCore import conversation

from pilotCore.handlers.welcome import keyboards, manage_data, static_text
from pilotCore.models import User, DriverUtils

from django_project.settings import TELEGRAM_TOKEN




def reg_operator(update: Update, context: CallbackContext) -> int:
    """Leave application to operator position"""
    text = 'Your application received'
    update.message.reply_text(
        text=text,
        reply_markup=None
    )
