from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [KeyboardButton(text="🔍 Ijaraga olaman"), KeyboardButton(text="➕ Ijaraga beraman")],
        [KeyboardButton(text="📂 Mening e'lonlarim")],
        [KeyboardButton(text="🇺🇿 | 🇷🇺 | 🇺🇸 | 🇰🇿"), KeyboardButton(text="❓ Qanday ishlaydi?")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def categories_kb():
    kb = [
        [KeyboardButton(text="🏢 Kvartira"), KeyboardButton(text="🏠 Uy hovli")],
        [KeyboardButton(text="💼 Ofis"), KeyboardButton(text="🏡 Dacha")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def delete_inline(ad_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 O'chirish", callback_query_data=f"del_{ad_id}")]
    ])