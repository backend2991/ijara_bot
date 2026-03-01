from aiogram.fsm.state import State, StatesGroup

class AdCreation(StatesGroup):
    building_type = State()
    duration = State()
    region = State()
    district = State()
    rooms = State()
    area = State()
    repair = State()
    amenities = State()
    photos = State()
    phone = State()