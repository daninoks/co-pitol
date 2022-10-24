import time

from telegram import ParseMode, Update, ForceReply, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from pilotCore import conversation

from pilotCore.handlers.customer import keyboards, manage_data, static_text
from pilotCore.models import User, DriverUtils

from django_project.settings import TELEGRAM_TOKEN
