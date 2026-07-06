import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "streamer_bot")
    
    BASE_DIR = Path(__file__).parent.parent
    VIDEO_DIR = BASE_DIR / "videos"
    LOG_DIR = BASE_DIR / "logs"

    # Create directories if they don't exist
    VIDEO_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
