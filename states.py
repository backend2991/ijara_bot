from aiogram.fsm.state import StatesGroup, State

class AdStates(StatesGroup):
    type = State()
    location = State()
    rooms_and_area = State()
    price = State()
    description = State()
    photo = State()
    phone = State()