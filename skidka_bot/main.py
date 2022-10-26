from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils import executor
import sqlite3
from buttons.keyboard_button import inline_start_kb
from config import TOKEN
from database import db_admin
from database.db_admin import check_user_in_db

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db_admin.sql_start()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if check_user_in_db(message.from_user.id) == None:
        await message.answer("Привет.Я бот для контроля за скидками WildBerries.Оправь мне ссылку на желаемый товар, "
                             "а я уведомлю тебя, когда цена на товар снизится.", reply_markup=inline_start_kb,
                             )
        client = message.from_user.id
        name = message.from_user.first_name

        base = sqlite3.connect('database/skidka.db')
        cur = base.cursor()
        sql = """INSERT INTO users (user_id, user_name) VALUES(?,?)"""
        params = (client, name)
        cur.execute(sql, params)
        base.commit()
    else:
        await message.answer("И снова здравствуйте!", reply_markup=inline_start_kb)


@dp.callback_query_handler(text='url_button')
async def send_start_url(callback: CallbackQuery):
    await callback.answer(
        text="Ты пидор  😎 ",
        show_alert=True
    )


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
