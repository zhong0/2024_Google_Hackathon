from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="frontend")

resource_dir = Path(__file__).parent / "resource"
app.mount("/resource", StaticFiles(directory=resource_dir), name="resource")
upload_dir = Path(__file__).parent / "upload"
app.mount("/upload", StaticFiles(directory=upload_dir), name="upload")
frontend_dir = Path(__file__).parent / "frontend"
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = {"name": "Zhongzhong"}
    return templates.TemplateResponse("homepage.html", {"request": request, "name": data["name"]})

@app.get("/fitting_style", response_class=HTMLResponse)
async def fitting_style(request: Request):
    return templates.TemplateResponse("fittingstyle.html", {"request": request})