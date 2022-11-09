from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_button1 = InlineKeyboardButton('🔗 Отправить ссылку на товар 🔗', callback_data='url_button')
check_items = InlineKeyboardButton('📦 Посмотреть мои товары 📦', callback_data='package_button')
help_button = InlineKeyboardButton('ℹ️ Помощь ℹ️', callback_data='help_button')
delete_button = InlineKeyboardButton('🗑 Удалить один товар из списка отслеживаемых ️🗑️', callback_data='delete_button')
personal_sale_button = InlineKeyboardButton('%💲 Ввести свою персональную скидку 💲%',
                                            callback_data='personal_sale_button')
delete_all = InlineKeyboardButton('☢️☢️❗️Удалить все товары из списка ☢️☢️❗️',
                                  callback_data='delete_all_button')
confirm_delete_button = InlineKeyboardButton('✅ Да, удалить всё ✅', callback_data='confirm_button')
cancel_confirm_button = InlineKeyboardButton("❌ Отмена ❌", callback_data='cancel_confirm_button')

cancel_button = KeyboardButton('♻️Вернуться в меню ♻')

inline_start_kb = InlineKeyboardMarkup().add(start_button1).add(check_items).add(
    delete_button).add(help_button).add(delete_all)

delete_all_kb = InlineKeyboardMarkup().add(confirm_delete_button).add(cancel_confirm_button)
call_cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel_button)