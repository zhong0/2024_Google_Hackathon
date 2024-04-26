from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from backend.api.Router import api_router

app = FastAPI()
app.include_router(api_router)

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
    return templates.TemplateResponse("fittingStyleOcca.html", {"request": request})

@app.get("/fitting_clothes", response_class=HTMLResponse)
async def fitting_clothes(request: Request):
    return templates.TemplateResponse("fittingClothes.html", {"request": request})

@app.get("/fitting_result", response_class=HTMLResponse)
async def fitting_result(request: Request):
    return templates.TemplateResponse("fittingResult.html", {"request": request})

@app.get("/explore", response_class=HTMLResponse)
async def explore(request: Request):
    return templates.TemplateResponse("explore.html", {"request": request})

@app.get("/explore_intro", response_class=HTMLResponse)
async def explore_intro(request: Request):
    return templates.TemplateResponse("exploreIntro.html", {"request": request})

@app.get("/piece_info", response_class=HTMLResponse)
async def piece_info(request: Request):
    return templates.TemplateResponse("pieceInfo.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/closet", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("closet.html", {"request": request})