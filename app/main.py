from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# 设置模板引擎
templates = Jinja2Templates(directory="frontend")

resource_dir = Path(__file__).parent / "resource"
app.mount("/resource", StaticFiles(directory=resource_dir), name="resource")
resource_dir = Path(__file__).parent / "upload"
app.mount("/upload", StaticFiles(directory=resource_dir), name="upload")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    data = {"name": "Zhongzhong"}
    # 渲染 HTML 模板并返回
    return templates.TemplateResponse("homepage.html", {"request": request, "name": data["name"]})