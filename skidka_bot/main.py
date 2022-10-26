from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils import executor

from buttons.keyboard_button import inline_start_kb
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет.Я бот для контроля за скидками WildBerries.Оправь мне ссылку на желаемый товар, "
                         "а я уведомлю тебя, когда цена на товар снизится.", reply_markup=inline_start_kb,
                         )


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
