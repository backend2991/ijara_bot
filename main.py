import asyncio
import logging
import sys
import aiosqlite
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# --- 1. LOGGING VA KONFIGURATSIYA ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

TOKEN = "8222917234:AAGxqndfNnBAzh9lS8HrYeNuABz3YNINSJQ"
ADMINS = [8584543342]
PROXY_URL = 'http://proxy.server:3128'

# --- 2. FSM HOLATLARI ---
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

# --- 3. TUGMALAR GENERATORI ---
def get_universal_kb(items: list, prefix: str, cols: int = 3):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=str(item), callback_data=f"{prefix}_{item}"))
    builder.adjust(cols)
    return builder.as_markup()

def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Ijaraga olaman"), KeyboardButton(text="Ijaraga beraman")],
        [KeyboardButton(text="Mening e'lonlarim")]
    ], resize_keyboard=True)

def amenities_kb(selected_items: list):
    all_items = [
        "Konditsioner", "Muzlatgich", "Televizor", "Kir yuvish m.", "Wi-Fi", 
        "Lift", "Mebel", "Mikroto'lqinli pech", "Idish yuvish m.", "Vanna", 
        "Balkon", "Avtoturargoh", "Maktab yaqin", "Bog'cha yaqin", "Metro yaqin", 
        "Bozor yaqin", "Domofon", "Xavfsizlik", "Hovuz", "Sauna"
    ]
    builder = InlineKeyboardBuilder()
    for item in all_items:
        if item not in selected_items:
            builder.add(InlineKeyboardButton(text=item, callback_data=f"amenity_{item}"))
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="✅ TASDIQLASH", callback_data="amenity_done"))
    return builder.as_markup()

# --- 4. MA'LUMOTLAR BAZASI ---
async def creat_table():
    async with aiosqlite.connect("rental_bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                b_type TEXT, duration TEXT, region TEXT, district TEXT,
                rooms TEXT, area TEXT, repair TEXT, amenities TEXT,
                photo_id TEXT, phone TEXT, status TEXT DEFAULT 'active'
            )
        """)
        await db.commit()

# --- 5. BOT VA DISPATCHER ---
session = AiohttpSession(proxy=PROXY_URL)
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

# --- 6. HANDLERLAR (MANTIQ) ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Xush kelibsiz! Bo'limni tanlang:", reply_markup=main_menu())

@dp.message(F.text == "Ijaraga beraman")
async def start_ad(message: types.Message, state: FSMContext):
    await state.set_state(AdCreation.building_type)
    types_list = ["Kvartira", "Hovli", "Ofis", "Dacha", "Do'kon", "Bino", "Podval"]
    await message.answer("🏠 Bino turini tanlang:", reply_markup=get_universal_kb(types_list, "type", 2))

@dp.callback_query(AdCreation.building_type)
async def set_type(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(building_type=call.data.split("_")[1])
    await state.set_state(AdCreation.duration)
    await call.message.edit_text("⏱ Ijara muddatini tanlang:", 
                                 reply_markup=get_universal_kb(["Kunlik", "Oylik", "Uzoq muddatli"], "dur", 2))

@dp.callback_query(AdCreation.duration)
async def set_duration(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(duration=call.data.split("_")[1])
    await state.set_state(AdCreation.region)
    regions = ["Toshkent sh.", "Toshkent vil.", "Samarqand", "Buxoro", "Andijon", "Farg'ona", "Namangan"]
    await call.message.edit_text("📍 Viloyatni tanlang:", reply_markup=get_universal_kb(regions, "reg", 2))

@dp.callback_query(AdCreation.region)
async def set_region(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=call.data.split("_")[1])
    await state.set_state(AdCreation.district)
    districts = ["Chilonzor", "Yunusobod", "M.Ulug'bek", "Mirobod", "Shayxontohur", "Olmazor", "Sergeli", "Uchtepa", "Yashnobod", "Bektemir"]
    await call.message.edit_text("🏙 Tumanni tanlang:", reply_markup=get_universal_kb(districts, "dist", 2))

@dp.callback_query(AdCreation.district)
async def set_district(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(district=call.data.split("_")[1])
    await state.set_state(AdCreation.rooms)
    await call.message.edit_text("🚪 Xonalar sonini tanlang:", reply_markup=get_universal_kb(list(range(1, 11)), "room", 4))

@dp.callback_query(AdCreation.rooms)
async def set_rooms(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(rooms=call.data.split("_")[1])
    await state.set_state(AdCreation.area)
    areas = [f"{i} m²" for i in range(20, 220, 10)]
    await call.message.edit_text("📐 Maydonni tanlang:", reply_markup=get_universal_kb(areas, "area", 3))

@dp.callback_query(AdCreation.area)
async def set_area(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(area=call.data.split("_")[1])
    await state.set_state(AdCreation.repair)
    repairs = ["Evro", "Lux", "O'rtacha", "Ta'mirtalab", "Yangi", "Kosmetik"]
    await call.message.edit_text("🛠 Remont holati:", reply_markup=get_universal_kb(repairs, "rep", 2))

@dp.callback_query(AdCreation.repair)
async def set_repair(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(repair=call.data.split("_")[1], selected_amenities=[])
    await state.set_state(AdCreation.amenities)
    await call.message.edit_text("✨ Qulayliklarni tanlang (kamida 1 ta):", reply_markup=amenities_kb([]))

@dp.callback_query(AdCreation.amenities, F.data.startswith("amenity_"))
async def set_amenities(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("selected_amenities", [])
    action = call.data.split("_")[1]

    if action == "done":
        if not selected:
            await call.answer("Hech bo'lmasa 1 ta qulaylik tanlang!", show_alert=True)
            return
        await state.update_data(amenities=", ".join(selected))
        await state.set_state(AdCreation.photos)
        await call.message.delete()
        await call.message.answer("📸 Uy rasmini yuboring (1 ta rasm kifoya):")
    else:
        selected.append(action)
        await state.update_data(selected_amenities=selected)
        logger.info(f"User {call.from_user.id} added {action}")
        await call.message.edit_reply_markup(reply_markup=amenities_kb(selected))

@dp.message(AdCreation.photos, F.photo)
async def set_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(AdCreation.phone)
    await message.answer("📞 Telefon raqamingizni yuboring (yoki yozing):")

@dp.message(AdCreation.phone)
async def finalize_ad(message: types.Message, state: FSMContext):
    data = await state.get_data()
    async with aiosqlite.connect("rental_bot.db") as db:
        await db.execute("""
            INSERT INTO ads (user_id, b_type, duration, region, district, rooms, area, repair, amenities, photo_id, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (message.from_user.id, data['building_type'], data['duration'], data['region'], 
              data['district'], data['rooms'], data['area'], data['repair'], 
              data['amenities'], data['photo_id'], message.text))
        await db.commit()
    
    logger.info(f"User {message.from_user.id} e'lonni muvaffaqiyatli joyladi.")
    await state.clear()
    await message.answer("✅ E'loningiz saqlandi va tez orada e'lon qilinadi!", reply_markup=main_menu())

@dp.message(F.text == "Mening e'lonlarim")
async def show_my_ads(message: types.Message):
    async with aiosqlite.connect("rental_bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM ads WHERE user_id = ?", (message.from_user.id,)) as cursor:
            ads = await cursor.fetchall()
            
    if not ads:
        await message.answer("Sizda hali e'lonlar mavjud emas.")
        return

    for ad in ads:
        caption = (f"🏠 {ad['b_type']} ({ad['duration']})\n"
                   f"📍 {ad['region']}, {ad['district']}\n"
                   f"🛏 Xonalar: {ad['rooms']} | 📏 Maydon: {ad['area']}\n"
                   f"🛠 Remont: {ad['repair']}\n"
                   f"✨ Qulayliklar: {ad['amenities']}\n"
                   f"📞 Aloqa: {ad['phone']}")
        await message.answer_photo(photo=ad['photo_id'], caption=caption)

# --- 7. ASOSIY ISHGA TUSHIRISH ---
async def main():
    await creat_table()
    logger.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot to'xtatildi")