import aiosqlite

DB_NAME = "rent_bot.db"

async def init_db():
    db = await aiosqlite.connect(DB_NAME)
    await db.execute("""
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            category TEXT,
            location TEXT,
            rooms TEXT,
            price TEXT,
            description TEXT,
            photo_id TEXT,
            phone TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    await db.commit()
    await db.close()

async def add_ad(data: dict, owner_id: int):
    db = await aiosqlite.connect(DB_NAME)
    await db.execute("""
        INSERT INTO ads (owner_id, category, location, rooms, price, description, photo_id, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (owner_id, data['category'], data['location'], data['rooms'], 
          data['price'], data['description'], data['photo'], data['phone']))
    await db.commit()
    await db.close()

async def get_my_ads(user_id: int):
    db = await aiosqlite.connect(DB_NAME)
    cursor = await db.execute("SELECT id, category, price, location FROM ads WHERE owner_id = ?", (user_id,))
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()
    return rows

async def delete_ad(ad_id: int):
    db = await aiosqlite.connect(DB_NAME)
    await db.execute("DELETE FROM ads WHERE id = ?", (ad_id,))
    await db.commit()
    await db.close()