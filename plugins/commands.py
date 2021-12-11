# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .info import get_movie

START_TEXT = """Hello {}
I am Star Movie and I am a bot And I Used to Find information about Movies.

> `I can find information of all movies.`

Made by @TeamThunderSupport"""

JOIN_BUTTONS = [
    InlineKeyboardButton(
        text='🚀 Join Bots Updates Channel 🚀',
        url='https://t.me/thunderprojectsupdates'
    ),
    InlineKeyboardButton(
        text='🔥 Join our Group🔥',
        url='https://t.me/thundergotechnologysupport'
    )    
]

BUTTONS = InlineKeyboardMarkup(
    [JOIN_BUTTONS]
)

@Client.on_message(filters.private & filters.command(["start"]), group=-1)
async def start(bot, update):
    if update.text == "/start":
        await update.reply_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
    else:
        movie = update.text.split(" ", 1)[1]
        await get_movie(bot, update, movie)
