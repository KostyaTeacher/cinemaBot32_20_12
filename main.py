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
    # kb = [
    #     [types.KeyboardButton(text="Buton1")],
    #     [types.KeyboardButton(text="Buton2")]
    # ]
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Text on field")
    # await message.answer("Which button push?", reply_markup=keyboard)
    film_choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Button1", callback_data="Button1")
    film_choice.add(button)
    button = InlineKeyboardButton(text="Кнопка 2", callback_data="Button2")
    film_choice.add(button)
    button = InlineKeyboardButton(text="Кнопка 3", callback_data="Button3")
    film_choice.add(button)
    await message.answer(text='Привіт! Я - бот-кіноафіша🍿\nОбери фільм, про який ти хочеш дізнатися.',
                         reply_markup=film_choice)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
