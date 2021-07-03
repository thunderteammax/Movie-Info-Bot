# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


API = 'https://api.sumanjay.cf/watch/'


@Client.on_message(filters.command(["info", "information"]))
async def get_command(bot, update):
    movie = update.text.split(" ", 1)
    movie = movie.replace(" ", "+")
    movie = movie.replace("\n", "+")
    keyboard = [
        InlineKeyboardButton(
            text="Click here",
            url=f"https://telegram.me/{username}?start={movie}"
        )
    ]
    await update.reply_text(
        text=f"Click the button below",
        reply_markup=InlineKeyboardMarkup([keyboard]),
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def get_movie_name(bot, update):
    await get_movie(bot, update, update.text)


async def get_movie(bot, update, movie):
    movie_name = movie.replace(" ", "+")
    movie_name = movie_name.replace("\n", "+")
    response = requests.get(API + movie_name)
    movies = response.json()
    keyboard = []
    for movie in movies:
        data = "movie+"
        data += movie['title'].replace(" ", "_")
        data += "+"
        data += movie['type'].replace(" ", "_")
        data += "+"
        data += str(movie['release_year'])
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{movie['title']} - {movie['type']}",
                    callback_data=data
                )
            ]
        )
    await update.reply_text(
        text="Select required option",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
        quote=True
    )


async def cb_edit(bot, update, movie, type, year):
    movie_name = movie.replace("_", "+")
    response = requests.get(API + movie_name)
    movies = response.json()
    title = movie.replace("_", " ")
    type_movie = type.replace("_", " ")
    for i in movies:
        if (title in i['title'] or i['title'] in title) and (type_movie in i['type'] or i['type'] in type_movie) and (year in str(i['release_year']) or str(i['release_year']) in year):
            try:
                text = info(movie)
            except Exception as error:
                text = error
    await update.edit_text(
        text=info,
        disable_web_page_preview=True
    )


def info(movie):
    info = f"Title: {movie['title']}\n"
    info += f"Type: {movie['type']}\n"
    if movie['providers']:
        try:
            providers = movie['providers']
            info += f"Providers:"
            providers = movie['providers']
            for provider in providers:
                info += f" [{provider}]({providers[provider]})"
            info += "\n"
        except:
            pass
    try:
        info += f"Release Date: {str(movie['release_date'])}\n"
    except:
        pass
    try:
        info += f"Release Year: {movie['release_year']}\n"
    except:
        pass
    try:
        if movie['score']:
            scores = movie['score']
            info += "Score:"
            for score in scores:
                info += f" {score} - {str(scores[score])}"
    except:
        pass
    return info


def thumb(movie):
    thumbnail = movie['movie_thumb']
    return thumbnail
