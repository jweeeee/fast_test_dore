from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil, os, json

app = FastAPI()

# static 폴더 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 경로들
DATA_PATH = "data/images.json"
IMAGE_DIR = "static/images"

# JSON 로드
def load_image_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# JSON 저장
def save_image_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def index():
    images = load_image_data()
    html = """
    <html><head><title>사진 리스트</title></head><body>
    <h1>📷 사진 리스트</h1><div style='display:flex; flex-direction:column; gap:10px;'>
    """
    for img in images:
        html += f'<img src="/static/images/{img}" width="300">'
    html += """
    </div><hr><h2>📤 사진 업로드</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <button type="submit">업로드</button>
    </form></body></html>
    """
    return HTMLResponse(content=html)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    file_path = os.path.join(IMAGE_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    images = load_image_data()
    images.append(file.filename)
    save_image_data(images)

    return {"message": "업로드 완료", "filename": file.filename}
