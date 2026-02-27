import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import db as db_manager
from states import AdCreation
import buttons as kb

TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=kb.main_menu())

@dp.message(F.text == "➕ Ijaraga beraman")
async def start_ad(message: types.Message, state: FSMContext):
    await state.set_state(AdCreation.category)
    await message.answer("Turini tanlang:", reply_markup=kb.categories_kb())

@dp.message(AdCreation.category)
async def set_cat(message: types.Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        return await message.answer("Bekor qilindi.", reply_markup=kb.main_menu())
    await state.update_data(category=message.text)
    await state.set_state(AdCreation.location)
    await message.answer("Manzilni yozing:", reply_markup=types.ReplyKeyboardRemove())

@dp.message(AdCreation.location)
async def set_loc(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(AdCreation.rooms)
    await message.answer("Xonalar va maydon:")

@dp.message(AdCreation.rooms)
async def set_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(AdCreation.price)
    await message.answer("Narxi:")

@dp.message(AdCreation.price)
async def set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AdCreation.description)
    await message.answer("Tavsif:")

@dp.message(AdCreation.description)
async def set_desc(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AdCreation.photo)
    await message.answer("Rasm yuboring:")

@dp.message(AdCreation.photo, F.photo)
async def set_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AdCreation.phone)
    await message.answer("Telefon raqam:")

@dp.message(AdCreation.phone)
async def set_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['phone'] = message.text
    await db_manager.add_ad(data, message.from_user.id)
    await message.answer("E'lon saqlandi!", reply_markup=kb.main_menu())
    await state.clear()

# --- Mening e'lonlarim ---
@dp.message(F.text == "📂 Mening e'lonlarim")
async def my_ads(message: types.Message):
    ads = await db_manager.get_my_ads(message.from_user.id)
    if not ads:
        return await message.answer("E'lonlar yo'q.")
    
    for ad in ads:
        text = f"E'lon #{ad[0]}\nTur: {ad[1]}\nNarx: {ad[2]}\nJoy: {ad[3]}"
        await message.answer(text, reply_markup=kb.delete_inline(ad[0]))

@dp.callback_query(F.data.startswith("del_"))
async def del_ad_call(call: types.CallbackQuery):
    ad_id = int(call.data.split("_")[1])
    await db_manager.delete_ad(ad_id)
    await call.answer("O'chirildi")
    await call.message.delete()

async def main():
    await db_manager.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())