import aiosqlite

async def init_db():
    async with aiosqlite.connect("rent_bot.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                building_type TEXT,
                duration TEXT,
                region TEXT,
                district TEXT,
                rooms TEXT,
                area TEXT,
                repair TEXT,
                amenities TEXT,
                photos TEXT,
                phone TEXT,
                status TEXT DEFAULT 'active'
            )
        """)
        await db.commit()

async def save_ad(data, user_id):
    async with aiosqlite.connect("rent_bot.db") as db:
        await db.execute("""
            INSERT INTO ads (user_id, building_type, duration, region, district, rooms, area, repair, amenities, photos, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, data['building_type'], data['duration'], data['region'], 
              data['district'], data['rooms'], data['area'], data['repair'], 
              data['amenities'], data['photos'], data['phone']))
        await db.commit()

async def get_user_ads(user_id):
    async with aiosqlite.connect("rent_bot.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM ads WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchall()