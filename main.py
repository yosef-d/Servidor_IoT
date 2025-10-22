from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import json, os, datetime

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_data(request: Request):
    data = await request.json()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(DATA_FOLDER, f"data_{timestamp}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return {"status": "ok", "saved_as": filename}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/json", filename=filename)
    return {"error": "Archivo no encontrado"}
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
