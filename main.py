import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from db import db, amenities_kb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

TOKEN = "8617267923:AAFem8KDMKHt1mBUCEesamTxsWSME-5aSJY"
PROXY_URL = 'http://proxy.server:3128'

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

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Ijaraga olaman"), KeyboardButton(text="Ijaraga beraman")],
        [KeyboardButton(text="🇺🇿 | 🇷🇺 | 🇺🇸 | 🇰🇿"), KeyboardButton(text="Qanday ishlaydi?")],
        [KeyboardButton(text="📈 Reklama"), KeyboardButton(text="Mening e'lonlarim")]
    ], resize_keyboard=True)

def get_reply_kb(items: list, cols: int = 2):
    keyboard = []
    row = []
    for item in items:
        row.append(KeyboardButton(text=str(item)))
        if len(row) == cols:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

session = AiohttpSession(proxy=PROXY_URL)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Xush kelibsiz!", reply_markup=get_main_menu())

@dp.message(F.text == "Mening e'lonlarim")
async def show_my_ads(message: types.Message):
    ads = await db.get_user_ads(message.from_user.id)
    if not ads:
        await message.answer("Sizda e'lonlar yo'q.")
        return
    for ad in ads:
        caption = (f"🏠 {ad['b_type']} | {ad['duration']}\n📍 {ad['region']}, {ad['district']}\n"
                   f"🛏 {ad['rooms']} xona | 📐 {ad['area']}\n🛠 {ad['repair']}\n📞 {ad['phone']}")
        await message.answer_photo(photo=ad['photo_id'], caption=caption)

@dp.message(F.text == "Ijaraga beraman")
async def start_ad(message: types.Message, state: FSMContext):
    await state.set_state(AdCreation.building_type)
    await message.answer("Bino turini tanlang:", reply_markup=get_reply_kb(["Kvartira", "Hovli", "Ofis", "Dacha", "Do'kon"]))

@dp.message(AdCreation.building_type)
async def set_type(message: types.Message, state: FSMContext):
    await state.update_data(building_type=message.text)
    await state.set_state(AdCreation.duration)
    await message.answer("Muddatni tanlang:", reply_markup=get_reply_kb(["Kunlik", "Oylik", "Uzoq muddatli"]))

@dp.message(AdCreation.duration)
async def set_duration(message: types.Message, state: FSMContext):
    await state.update_data(duration=message.text)
    await state.set_state(AdCreation.region)
    await message.answer("Viloyatni tanlang:", reply_markup=get_reply_kb(["Toshkent sh.", "Toshkent vil.", "Samarqand", "Andijon"]))

@dp.message(AdCreation.region)
async def set_region(message: types.Message, state: FSMContext):
    await state.update_data(region=message.text)
    await state.set_state(AdCreation.district)
    await message.answer("Tumanni tanlang:", reply_markup=get_reply_kb(["Chilonzor", "Yunusobod", "Mirobod", "Uchtepa", "Sergeli"]))

@dp.message(AdCreation.district)
async def set_district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AdCreation.rooms)
    await message.answer("Xonalar soni:", reply_markup=get_reply_kb([str(i) for i in range(1, 11)], 4))

@dp.message(AdCreation.rooms)
async def set_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(AdCreation.area)
    await message.answer("Maydonni tanlang:", reply_markup=get_reply_kb([f"{i} m²" for i in range(20, 220, 20)], 3))

@dp.message(AdCreation.area)
async def set_area(message: types.Message, state: FSMContext):
    await state.update_data(area=message.text)
    await state.set_state(AdCreation.repair)
    await message.answer("Remont holati:", reply_markup=get_reply_kb(["Evro", "Lux", "O'rtacha", "Toza", "Ta'mirtalab"]))

@dp.message(AdCreation.repair)
async def set_repair(message: types.Message, state: FSMContext):
    await state.update_data(repair=message.text)
    await state.set_state(AdCreation.amenities)
    await message.answer("Qulayliklarni yozing (Konditsioner, Wi-Fi...):", reply_markup=amenities_kb)

@dp.message(AdCreation.amenities)
async def set_amenities(message: types.Message, state: FSMContext):
    await state.update_data(amenities=message.text)
    await state.set_state(AdCreation.photos)
    await message.answer("Uy rasmiga yuboring:")

@dp.message(AdCreation.photos, F.photo)
async def set_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(AdCreation.phone)
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Kontakt", request_contact=True)]], resize_keyboard=True)
    await message.answer("Telefon raqamingizni yuboring:", reply_markup=kb)

@dp.message(AdCreation.phone, F.contact | F.text)
async def finalize(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    data = await state.get_data()
    await db.save_ad(message.from_user.id, data, phone)
    await state.clear()
    await message.answer("✅ E'loningiz saqlandi!", reply_markup=get_main_menu())

async def main():
    await db.connect()
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())