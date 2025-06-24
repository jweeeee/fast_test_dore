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
    <html><head><title>도르리 대전 수제 케이크</title>
    <style>
      body{font-family:sans-serif;background-color:#fef8ec}
      h4{font:pink}
      .img-wrap{display:flex;flex-direction:column;gap:15px;margin-top:20px}
      .fixed-links{position:fixed;right:20px;bottom:20px;background:#eee;padding:10px;border-radius:8px}
    </style></head><body>
    <div style=''>
    <img src='/static/images/logo.jpeg' width='100' style='display:inline-block'>
    <div style='display:inline-block'><h1>도르리 대전앙금플라워떡케이크.</h1>
    <h4>수제 앙금 플라워케이크 도르리입니다.</h4>
    </div>
    </div>
    <br><br><br>
    <h4>케이크디자인</h4>
    <hr>
    
    <div class="img-wrap">
   
    """
    for img in images:
        html += f'<img src="/static/images/{img}" width="300">'
    html += """
      </div>
     <br><br><br>
    <h4>클래스 안내</h4>
    <hr>
     <br><br><br>
    <h4>한식 디저트</h4>
    <hr>
     <br><br><br>
    <h4>답례품/선물세트</h4>
    <hr>
     <br><br><br>
    <h4>앙금플라워케이크</h4>
    <hr>
    
  
    <div class="fixed-links">
      <a href="https://instagram.com" style="border-radius:300px">인스타그램연결</a><br>
      <a href="https://open.kakao.com" style="border-radius:300px">카카오오픈톡연결</a>
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
      <input type="file" name="file" accept="image/*" style="width: 40%; height: 20%; font-size: 1rem;"><br><br>
      <button type="submit" style="width: 40%; height: 20%; font-size: 1rem;">업로드</button>
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
