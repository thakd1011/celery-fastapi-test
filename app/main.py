from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from celery import Celery

from config import CONFIG_GLOB

app = FastAPI()
app.mount("/static", StaticFiles(directory=CONFIG_GLOB.STATIC_DATA_PATH), name="static")

# Set up templates and static files
templates = Jinja2Templates(directory=CONFIG_GLOB.TEMPLATE_PATH)

# Directory to store recorded audio
DATA_DIR = Path(CONFIG_GLOB.SENSOR_DATA_PATH_R)
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    files = list(DATA_DIR.glob("*.m4a"))  # Adjust file type as needed
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "files": files})

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    file_location = DATA_DIR / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"File '{file.filename}' uploaded successfully."}


celery_app = Celery('tasks', broker=CONFIG_GLOB.REDIS_URL)

@app.post("/analyze/")
async def analyze(file_name: str):
    analyze_task = celery_app.send_task('worker_analyze.analyze', args=[file_name])
    return {"task_id": analyze_task.id}

@app.post("/preprocessing/")
async def preprocess_data(data):
    preprocess_task = celery_app.send_task('worker_preprocess.preprocess', args=data)
    return {"task_id": preprocess_task.id}
