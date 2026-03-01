from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Umumiy generator
def get_universal_kb(items: list, prefix: str, cols: int = 3):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(InlineKeyboardButton(text=str(item), callback_data=f"{prefix}_{item}"))
    builder.adjust(cols)
    return builder.as_markup()

# 1. Bino turi (building_type)
def building_type_kb():
    types = ["Kvartira", "Hovli", "Ofis", "Dacha", "Do'kon", "Omborxona", "Yer uchastkasi", "Bino", "Podval", "Mansarda"]
    return get_universal_kb(types, "type", cols=2)

# 2. Ijara muddati (duration)
def duration_kb():
    durations = ["Kunlik", "Haftalik", "Oylik", "6 oy", "1 yil", "Uzoq muddatli", "Faqat iyul-avgust", "Mavsumiy"]
    return get_universal_kb(durations, "dur", cols=2)

# 3. Viloyat (region) - 14 ta hudud
def region_kb():
    regions = [
        "Toshkent sh.", "Toshkent vil.", "Samarqand", "Buxoro", "Andijon", "Farg'ona", 
        "Namangan", "Navoiy", "Qashqadaryo", "Surxondaryo", "Jizzax", "Sirdaryo", "Xorazm", "Qoraqalpog'iston"
    ]
    return get_universal_kb(regions, "reg", cols=2)

# 4. Tuman (district) - 20 ta variant
def district_kb():
    districts = [
        "Chilonzor", "Yunusobod", "M.Ulug'bek", "Mirobod", "Shayxontohur", "Olmazor", 
        "Sergeli", "Yakkasaroy", "Uchtepa", "Bektemir", "Yashnobod", "Yangihayot", 
        "Qibray", "Zangiota", "Chirchiq", "G'azalkent", "Keles", "Nazarbek", "To'ytepa", "Piskent"
    ]
    return get_universal_kb(districts, "dist", cols=2)

# 5. Xonalar soni (rooms)
def rooms_kb():
    rooms = [str(i) for i in range(1, 11)] + ["10+"]
    return get_universal_kb(rooms, "room", cols=4)

# 6. Maydon (area) - 20 ta variant
def area_kb():
    areas = [f"{i} m²" for i in range(20, 220, 10)]
    return get_universal_kb(areas, "area", cols=3)

# 7. Remont (repair)
def repair_kb():
    repairs = ["Evro", "Lux", "Neo-Classic", "High-tech", "O'rtacha", "Toza", "Ta'mirtalab", "Yangi", "Kosmetik", "Mualliflik loyihasi"]
    return get_universal_kb(repairs, "rep", cols=2)

# 8. Qulayliklar (amenities) - 20 ta variant (Multi-select)
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