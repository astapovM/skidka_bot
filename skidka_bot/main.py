from datetime import datetime

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import executor
import sqlite3

import database.db_admin
import states.set_states
from buttons.keyboard_button import inline_start_kb
from config import TOKEN
from database import db_admin
from database.db_admin import check_user_in_db

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db_admin.sql_start()
date = datetime.now().date()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if check_user_in_db(message.from_user.id) == None:
        await message.answer(f"Привет, {message.from_user.first_name}. Я - бот для отслеживания скидок."
                             f"Оставляй ссылку на товар - а я сообщу тебе,когда на него появится скидка",
                             reply_markup=inline_start_kb,
                             )
        client = message.from_user.id
        name = message.from_user.first_name

        base = sqlite3.connect('database/skidka.db')
        cur = base.cursor()
        sql = """INSERT INTO users (user_id, user_name, connect_date) VALUES(?,?,?)"""
        params = (client, name, date)
        cur.execute(sql, params)
        base.commit()
    else:
        await message.answer(f"{message.from_user.full_name}, калайсын есь жи", reply_markup=inline_start_kb)


@dp.callback_query_handler(text='url_button')
async def send_start_url(callback: CallbackQuery):
    await states.set_states.Url_input.insert_url.set()
    await callback.message.answer("Введите ссылку на страницу товара >>>  ")

@dp.message_handler(state=states.set_states.Url_input.insert_url)
async def url_input_state(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
        print(message.text.split("/")[0])
        if message.text.split("/")[0] != 'https:':
            await message.answer("Введите ссылку в верном формате : (https://www.wildberries.ru/catalog/number/detail.aspx")
            await states.set_states.Url_input.insert_url.set()
        else:
            base = sqlite3.connect('database/skidka.db')
            cur = base.cursor()
            sql = """INSERT INTO packages (id, package_url) VALUES(?,?)"""
            user_id = message.chat.id
            params = (user_id, data['url'])
            cur.execute(sql, params)
            base.commit()
            await state.finish()



@dp.callback_query_handler(text='package_button')
async def send_start_package(callback: CallbackQuery):
    await callback.answer(
        text="Список товаров пуст. "
             "Кстати ты пидор 😎",
        show_alert=True

    )


@dp.callback_query_handler(text='help_button')
async def sent_start_help(callback: CallbackQuery):
    await callback.answer(
        text="Чтобы воспользоваться функционалом бота введи  /start или нажми кнопку из меню, пидор",
        show_alert=True
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)