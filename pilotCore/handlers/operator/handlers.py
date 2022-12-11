from telegram import Update
from telegram.ext import CallbackContext


def reg_operator(update: Update, context: CallbackContext) -> int:
    """Leave application to operator position"""
    text = 'Your application received'
    update.message.reply_text(
        text=text,
        reply_markup=None
    )
