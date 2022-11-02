from aiogram.dispatcher.filters.state import State, StatesGroup


class Url_input(StatesGroup):
    insert_url = State()
    insert_item_id = State()
    insert_discount = State()


