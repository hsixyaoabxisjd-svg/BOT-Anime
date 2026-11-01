import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
WORK_DIR = Path(os.getenv("WORK_DIR", str(BASE_DIR / "work")))
WORK_DIR.mkdir(exist_ok=True, parents=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
APP_NAME = "anime_dubber"
