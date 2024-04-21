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

@router.post("/occasion")
def get_all_occasion(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"occasion": service.get_occasion(username)}

@router.post("/file-path")
def get_all_file_path(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"file_path": service.get_file_path(username)}

@router.post("/file-path-by-category")
def get_all_file_path(username: str = Form(...), category: str = Form(...)):
    if username is None or category is None:
        raise HTTPException(status_code=400, detail="Username & category is required")
    return {"file_path": service.get_file_path_by_category(username, category)}

@router.post("/clothes-info", deprecated=True)
def get_all_clothes_info(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"clothes_info": service.get_all_clothes_info(username)}