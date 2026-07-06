from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import Config

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(Config.MONGO_URI)
        self.db = self.client[Config.DB_NAME]
        self.rtmp = self.db.rtmp
        self.videos = self.db.videos
        self.history = self.db.history

db = Database()
