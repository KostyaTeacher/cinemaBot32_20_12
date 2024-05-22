import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
USER = os.getenv("USER_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

ADMINS = [int(USER)]

with open("films.json", "r", encoding="utf-8") as file:
    films = json.load(file)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    film_choice = InlineKeyboardMarkup()
    for film in films:
        button = InlineKeyboardButton(text=film, callback_data=film)
        film_choice.add(button)

    logging.info(f"Користувач {message.from_user.first_name} з нікнеймом {message.from_user.username} "
                 f"натиснув команду {message.text}")

    await message.answer(text='Привіт! Я - бот-кіноафіша🍿\nОбери фільм, про який ти хочеш дізнатися.',
                         reply_markup=film_choice)


@dp.callback_query_handler()
async def get_film_info(callback_query: types.CallbackQuery):
    if callback_query.data in films.keys():
        await bot.send_photo(callback_query.message.chat.id, films[callback_query.data]["photo"],
                             "Постер фільму")
        url = films[callback_query.data]["site_url"]
        film_rating = films[callback_query.data]["rating"]
        film_description = films[callback_query.data]["description"]
        message = (f"<b>Film url: </b>{url}\n\n<b>About: </b>{film_description}\n\n"
                   f"<b>Rate: </b>{film_rating}")


        await bot.send_message(callback_query.message.chat.id, message, parse_mode="html")
    else:
        await bot.send_message(callback_query.message.chat.id, "Фільм не знайдено 😟")


@dp.message_handler(commands="add_film")
async def add_new_film(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMINS:
        await message.answer(text="Ведіть назву фільму, якій хочете додати.")
        await state.set_state("set_film_name")
    else:
        await message.answer(text="Недостатьно прав")


film_name = ""


@dp.message_handler(state="set_film_name")
async def set_film_name(message: types.Message, state: FSMContext):
    global film_name
    if len(message.text) > 64:
        await message.answer(text="Нажаль я не можу додати цей фільм (64 символи)")
    else:
        film_name = message.text
        films[film_name] = {}
        await state.set_state("set_site_url")
        await message.answer(text="Супер! Теперь введіть посилання на фільм")


@dp.message_handler(state="set_site_url")
async def set_site_url(message: types.Message, state: FSMContext):
    global film_name
    film_site_url = message.text
    films[film_name]["site_url"] = film_site_url
    await state.set_state("set_description")
    await message.answer(text="Чудово! Теперь розкажи про що фільм")


@dp.message_handler(state="set_description")
async def set_site_url(message: types.Message, state: FSMContext):
    global film_name
    film_description = message.text
    films[film_name]["description"] = film_description
    await state.set_state("set_rating")
    await message.answer(text="А який рейтінг у цього фільму?")


@dp.message_handler(state="set_rating")
async def set_rating(message: types.Message, state: FSMContext):
    global film_name
    film_rating = message.text
    films[film_name]["rating"] = film_rating
    await state.set_state("set_photo")
    await message.answer(text="Чудово! А тепер додай посилання на фото")


@dp.message_handler(state="set_photo")
async def set_rating(message: types.Message, state: FSMContext):
    global film_name
    film_photo = message.text
    films[film_name]["photo"] = film_photo
    with open("films.json", "w", encoding="utf-8") as file:
        json.dump(films, file, indent=4, ensure_ascii=False)
    print(films)
    await state.finish()
    await message.answer(text="Супер! Фільм додано до бібліотеки")


async def set_default_comands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Запустити бота"),
            types.BotCommand("add_film", "Додати новий фільм"),
        ]
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=set_default_comands)
