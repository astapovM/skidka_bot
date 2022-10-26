from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_button1 = InlineKeyboardButton('🔗 Отправить ссылку на товар', callback_data='url_button')
start_button2 = InlineKeyboardButton('📦 Посмотреть мои товары', callback_data='package_button')
start_button3 = InlineKeyboardButton('ℹ️ Помощь', callback_data='help_button')

inline_start_kb = InlineKeyboardMarkup().add(start_button1).add(start_button2).add(start_button3)
