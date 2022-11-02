from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_button1 = InlineKeyboardButton('🔗 Отправить ссылку на товар 🔗', callback_data='url_button')
check_items = InlineKeyboardButton('📦 Посмотреть мои товары 📦', callback_data='package_button')
help_button = InlineKeyboardButton('ℹ️ Помощь ℹ️', callback_data='help_button')
delete_button = InlineKeyboardButton('🗑 Удалить товар из списка отслеживаемых ️🗑️', callback_data='delete_button')
personal_sale_button = InlineKeyboardButton('%💲 Ввести свою персональную скидку 💲%', callback_data='personal_sale_button')

inline_start_kb = InlineKeyboardMarkup().add(start_button1).add(check_items).add(personal_sale_button).add(delete_button).add(help_button)

