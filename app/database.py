import sqlite3
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get base directory (root of project)
BASE_DIR = Path(__file__).resolve().parent.parent  # goes one level up from app/

# Get the relative DB path from env (with a default fallback)
relative_db_path = os.getenv("DATABASE_PATH")

# Build absolute path to the database
DB_PATH = BASE_DIR / relative_db_path

# Ensure the directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            content TEXT,
            download_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
