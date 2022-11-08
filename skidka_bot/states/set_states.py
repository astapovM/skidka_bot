from aiogram.dispatcher.filters.state import State, StatesGroup

#Сохранение ответов пользователя в fsm
class Url_input(StatesGroup):
    insert_url = State()
    insert_item_id = State()
    insert_discount = State()


