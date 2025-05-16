import qrcode
from pathlib import Path
from datetime import datetime
from app.database import get_db  # adjust this import if needed

QR_DIRECTORY = Path("static/qrcodes")
BASE_DIR = Path(__file__).resolve().parent.parent

QR_DIRECTORY = BASE_DIR / QR_DIRECTORY
QR_DIRECTORY.mkdir(parents=True, exist_ok=True)

def generate_qr(content: str, user_id: str = "default") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"qr_{user_id}_{timestamp}.png"
    file_path = QR_DIRECTORY / filename

    qr = qrcode.make(content)
    qr.save(file_path)

    relative_download_path = f"static/qrcodes/{filename}"

    with get_db() as conn:
        conn.execute(
            "INSERT INTO qr_codes (user_id, content, download_path) VALUES (?, ?, ?)",
            (user_id, content, relative_download_path)
        )

    return relative_download_path 

def get_user_history(user_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM qr_codes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        return cursor.fetchall()
