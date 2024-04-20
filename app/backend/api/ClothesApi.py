from fastapi import APIRouter, HTTPException, Form
from service.ClothService import ClothesService

router = APIRouter()
service = ClothesService()

@router.post("/category")
def get_all_category(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"category": service.get_category(username)}

@router.post("/style")
def get_all_style(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"style": service.get_style(username)}

@router.post("/scenario")
def get_all_scenario(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"scenario": service.get_scenario(username)}

@router.post("/file_path")
def get_all_file_path(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"file_path": service.get_file_path(username)}
