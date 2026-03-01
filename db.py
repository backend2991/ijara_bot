import aiosqlite

DB_NAME = "rental_bot.db"

class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        self.db = await aiosqlite.connect(DB_NAME)
        self.db.row_factory = aiosqlite.Row
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                b_type TEXT, duration TEXT, region TEXT, district TEXT,
                rooms TEXT, area TEXT, repair TEXT, amenities TEXT,
                photo_id TEXT, phone TEXT
            )
        """)
        await self.db.commit()

    async def save_ad(self, user_id, data, phone):
        query = """
            INSERT INTO ads (user_id, b_type, duration, region, district, rooms, area, repair, amenities, photo_id, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            user_id, data['building_type'], data['duration'], data['region'],
            data['district'], data['rooms'], data['area'], data['repair'],
            data['amenities'], data['photo_id'], phone
        )
        await self.db.execute(query, params)
        await self.db.commit()

    async def get_user_ads(self, user_id):
        cursor = await self.db.execute("SELECT * FROM ads WHERE user_id = ?", (user_id,))
        return await cursor.fetchall()

    async def close(self):
        if self.db:
            await self.db.close()

db = Database()