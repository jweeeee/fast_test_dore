from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil, os, json

app = FastAPI()

# 정적 파일 경로
app.mount("/static", StaticFiles(directory="fastapi_webapp/static"), name="static")

# 경로 설정
BASE_DIR = "fastapi_webapp"
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images")
DATA_PATH = os.path.join(BASE_DIR, "data", "images.json")

# 이미지 목록 불러오기
def load_images():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 이미지 목록 저장하기
def save_images(image_list):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(image_list, f, indent=2, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
async def index():
    images = load_images()
    html = """
    <html>
    <head>
        <title>랜딩 페이지</title>
        <style>
            .img-wrap { display: flex; flex-direction: column; gap: 10px; }
            .floating { position: fixed; bottom: 20px; right: 20px; background: #eee; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>📸 이미지 리스트</h1>
        <div class="img-wrap">
    """
    for img in images:
        html += f'<img src="/static/images/{img}" width="300">'
    html += """
        </div>
        <hr>
        <h2>📤 이미지 업로드</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">업로드</button>
        </form>
        <div class="floating">
            <a href="https://instagram.com" target="_blank">📷 인스타</a><br>
            <a href="https://open.kakao.com" target="_blank">💬 카톡</a>
        </div>
    </body>
    </html>
    """
    return html

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    file_path = os.path.join(IMAGE_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileo
