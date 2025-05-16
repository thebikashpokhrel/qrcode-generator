from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pathlib import Path
from app.database import init_db
from app.qrcode_utils import generate_qr, get_user_history
import os

app = FastAPI()

QR_DIRECTORY = Path("static/qrcodes")
BASE_DIR = Path(__file__).resolve().parent.parent

QR_DIRECTORY = BASE_DIR / QR_DIRECTORY
QR_DIRECTORY.mkdir(parents=True, exist_ok=True)

@app.on_event("startup")
def startup():
    init_db()

#comment
@app.post("/generate/")
async def create_qr(request: Request, content: str, user_id: str = "default"):
    try:
        file_path = generate_qr(content, user_id)
        filename = Path(file_path).name
        download_url = str(request.base_url) + f"download/{filename}"
        return {
            "filename": filename,
            "download_url": download_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_qr(filename: str):
    file_path = QR_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(file_path)

@app.get("/history/{user_id}")
async def history(user_id: str, request: Request):
    try:
        history = get_user_history(user_id)
        result = []
        for row in history:
            row_dict = dict(row)
            filename = Path(row_dict["download_path"]).name
            download_url = str(request.base_url) + f"download/{filename}"
            row_dict["download_url"] = download_url
            result.append(row_dict)
        return {"history": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#testcomment