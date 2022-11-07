from datetime import datetime

from states.set_states import Url_input

import parser_wb_page
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import executor
import sqlite3

from buttons.keyboard_button import inline_start_kb
from config import TOKEN
from database import db_admin
from database.db_admin import check_user_in_db, add_new_user, add_item_info, add_discount, add_new_price, take_url

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db_admin.sql_start()
date = datetime.now().date()
admin = 293427068


# Регистрируем пользователя при старте бота.
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if check_user_in_db(message.from_user.id) == None:
        await message.answer(f"Привет, {message.from_user.first_name}. Я - бот для отслеживания скидок."
                             f"Оставляй ссылку на товар - а я сообщу тебе,когда на него появится скидка",
                             reply_markup=inline_start_kb,
                             )
        params = (message.from_user.id, message.from_user.first_name, date)
        add_new_user(params)
    else:
        await message.answer(f"{message.from_user.full_name}, калайсын есь жи", reply_markup=inline_start_kb)


# Ловим ответ на нажатие инлайн кнопки "Отравить ссылку на товар"
@dp.callback_query_handler(text='url_button')
async def send_start_url(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer("•••••• ━───────────── • •• •• •• • ─────────────━ ••••••")
    await Url_input.insert_url.set()
    await callback.message.answer("Введите ссылку на страницу товара >>>  ")


# Проверяем ответ и сохраняем ссылку в БД
@dp.message_handler(state=Url_input.insert_url)
async def url_input_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['url'] = message.text
        if message.text.split("/")[0] != 'https:' and message.text:
            await message.answer(
                "Введите ссылку в верном формате : (https://www.wildberries.ru/catalog/number/detail.aspx")
            await Url_input.insert_url.set()


        else:
            item_info = parser_wb_page.page_parce(message.text)
            params = (message.chat.id, data['url'], item_info[0], item_info[1], item_info[2])
            try:
                add_item_info(params)
                await state.finish()
                await message.answer("Товар добавлен", reply_markup=inline_start_kb)
            except sqlite3.IntegrityError:
                await message.answer("Такой товар уже есть в вашем списке", reply_markup=inline_start_kb)
                await state.finish()


# Ловим ответ на нажатие инлайн кнопки "Посмотреть мои товары "
@dp.callback_query_handler(text='package_button')
async def send_start_package(callback: CallbackQuery):
    if db_admin.check_packages(callback.message.chat.id) != None:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.message.answer("•••••• ━───────────── • •• •• •• • ─────────────━ ••••••")
        package_list = db_admin.check_packages(callback.message.chat.id)
        for package in package_list:
            await callback.message.answer(
                f'{package[0]}.{package[1]}\n ※※※ <b>{package[2]} ※※※ {package[3]}</b> ※※※ <b>   Цена: {package[4]}</b>',
                parse_mode='html')

        await callback.message.answer("Ваш список товаров 😎", reply_markup=inline_start_kb)


    else:
        await callback.message.answer("Ваш список товаров пуст")


# Ловим ответ на нажатие инлайн кнопки "Помощь"
@dp.callback_query_handler(text='help_button')
async def send_start_help(callback: CallbackQuery):
    await callback.answer(
        text="Чтобы воспользоваться функционалом бота введите  /start или нажмите кнопку из меню",
        show_alert=True
    )


@dp.callback_query_handler(text='delete_button')
async def send_delete_button(callback: CallbackQuery):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await callback.message.answer("•••••• ━───────────── • •• •• •• • ─────────────━ ••••••")
    await callback.answer(
        text="Чтобы удалить товар из списка, введите его номер ",
        show_alert=True
    )
    package_list = db_admin.check_packages(callback.message.chat.id)
    for package in package_list:
        await callback.message.answer(
            f'{package[0]}.{package[1]}\n ※※※ <b>{package[2]} ※※※ {package[3]}</b> ※※※ <b>   Цена: {package[4]}</b>',
            parse_mode='html')
    await Url_input.insert_item_id.set()
    await callback.answer()


@dp.callback_query_handler(text='personal_sale_button')
async def personal_sale(callback: CallbackQuery):
    await callback.answer("Введите вашу персональную скидку, для более точного отображения цен на товары",
                          show_alert=True
                          )
    await callback.message.answer("введите скидку:    ")
    await Url_input.insert_discount.set()


@dp.message_handler(state=Url_input.insert_item_id)
async def url_input_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_to_delete'] = message.text
        db_admin.delete_item_from_db(message.text)
        await state.finish()
        await message.answer("Товар удалён из списка отслеживаемых", reply_markup=inline_start_kb)


@dp.message_handler(state=Url_input.insert_discount)
async def discount_input_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        discount = message.text
        db_admin.add_discount(message.from_user.id, discount)
        await state.finish()
        await message.answer(f"Персональная скидка составляет {discount}%", reply_markup=inline_start_kb)


@dp.message_handler(commands=['spam'])
async def spam(message):
    if message.from_user.id == admin:
        await bot.send_message(5670943281, 'Привет')


@dp.message_handler()
async def command_not_found(message: types.Message):
    await message.delete()
    await message.answer(f"Команда {message.text} не найдена")


# функция для отправки сообщения пользователям , при наличии скидки на товар
# async def message_to_users():
for url in take_url():
    url_for_update = (url[0])
    price_for_update = parser_wb_page.page_parce(url[0])[2]
    add_new_price(price_for_update, url_for_update)

# Создание задачи на ежедневный запуск парсера цены, и отправки сообщения пользователям.
# async def scheduler():
#     aioschedule.every().day.at("13:00").do(message_to_users, "message")
#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(10)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
