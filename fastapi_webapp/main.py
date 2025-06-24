from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil, os, json

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR  = os.path.join(BASE_DIR, "static", "images")
DATA_PATH  = os.path.join(BASE_DIR, "data", "images.json")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# ── 헬퍼 함수 ────────────────────────────────
def load_images():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_images(image_list):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(image_list, f, ensure_ascii=False, indent=2)

# ── 메인 페이지 ───────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index():
    images = load_images()
    html = """
    <html><head><title>메인 페이지</title>
    <style>
      body{font-family:sans-serif}
      .img-wrap{display:flex;flex-direction:column;gap:15px;margin-top:20px}
      .fixed-links{position:fixed;right:20px;bottom:20px;background:#eee;padding:10px;border-radius:8px}
    </style></head><body>
    <h1>🍽️ 우리 가게 메뉴 소개</h1>
    <div class="img-wrap">
      <img src="/static/images/sample1.jpg" width="300">
      <img src="/static/images/sample2.jpg" width="300">
      <img src="/static/images/sample3.jpg" width="300">
    """
    for img in images:
        html += f'<img src="/static/images/{img}" width="300">'
    html += """
    </div>
    <div class="fixed-links">
      <a href="https://instagram.com">📷 인스타</a><br>
      <a href="https://open.kakao.com">💬 카카오</a>
    </div>
    </body></html>
    """
    return html

# ── 관리자 페이지 ─────────────────────────────
@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    return """
    <html><head><title>관리자</title></head><body>
    <h2>이미지 업로드 (관리자 전용)</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*"><br><br>
      <button type="submit">업로드</button>
    </form>
    <p><a href="/">← 메인으로</a></p>
    </body></html>
    """

# ── 업로드 처리 ─────────────────────────────
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    file_path = os.path.join(IMAGE_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    images = load_images()
    images.append(file.filename)
    save_images(images)

    return HTMLResponse(f"<p>{file.filename} 업로드 완료</p><a href='/admin'>← 돌아가기</a>")
