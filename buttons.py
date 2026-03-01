from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_reply_kb(items: list, cols: int = 2):
    keyboard = []
    row = []
    for item in items:
        row.append(KeyboardButton(text=str(item)))
        if len(row) == cols:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Ijaraga olaman"), KeyboardButton(text="Ijaraga beraman")],
        [KeyboardButton(text="🇺🇿 | 🇷🇺 | 🇺🇸 | 🇰🇿"), KeyboardButton(text="Qanday ishlaydi?")],
        [KeyboardButton(text="📈 Reklama"), KeyboardButton(text="Mening e'lonlarim")]
    ], resize_keyboard=True)

def phone_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)

def building_type_kb():
    types = ["Kvartira", "Hovli", "Ofis", "Dacha", "Do'kon", "Omborxona", "Yer uchastkasi", "Bino", "Podval", "Mansarda"]
    return get_reply_kb(types, cols=2)

def duration_kb():
    durations = ["Kunlik", "Haftalik", "Oylik", "6 oy", "1 yil", "Uzoq muddatli", "Faqat iyul-avgust", "Mavsumiy"]
    return get_reply_kb(durations, cols=2)

def region_kb():
    regions = [
        "Toshkent sh.", "Toshkent vil.", "Samarqand", "Buxoro", "Andijon", "Farg'ona", 
        "Namangan", "Navoiy", "Qashqadaryo", "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"
    ]
    return get_reply_kb(regions, cols=2)

def district_kb():
    districts = [
        "Chilonzor", "Yunusobod", "M.Ulug'bek", "Mirobod", "Shayxontohur", "Olmazor", 
        "Sergeli", "Yakkasaroy", "Uchtepa", "Bektemir", "Yashnobod", "Yangihayot", 
        "Qibray", "Zangiota", "Chirchiq", "G'azalkent", "Keles", "Nazarbek", "To'ytepa", "Piskent"
    ]
    return get_reply_kb(districts, cols=2)

def rooms_kb():
    rooms = [str(i) for i in range(1, 11)] + ["10+"]
    return get_reply_kb(rooms, cols=4)

def area_kb():
    areas = [f"{i} m²" for i in range(20, 220, 10)]
    return get_reply_kb(areas, cols=3)

def repair_kb():
    repairs = ["Evro", "Lux", "Neo-Classic", "High-tech", "O'rtacha", "Toza", "Ta'mirtalab", "Yangi", "Kosmetik", "Mualliflik loyihasi"]
    return get_reply_kb(repairs, cols=2)

def amenities_kb():
    all_items = [
        "Konditsioner", "Muzlatgich", "Televizor", "Kir yuvish m.", "Wi-Fi", 
        "Lift", "Mebel", "Mikroto'lqinli pech", "Idish yuvish m.", "Vanna", 
        "Balkon", "Avtoturargoh", "Maktab yaqin", "Bog'cha yaqin", "Metro yaqin", 
        "Bozor yaqin", "Domofon", "Xavfsizlik", "Hovuz", "Sauna"
    ]
    return get_reply_kb(all_items, cols=2)