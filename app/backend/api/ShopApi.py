from fastapi import APIRouter, HTTPException, Form
from service.ShopService import ShopService

router = APIRouter()
shop_service = ShopService()

@router.post("/clothes-info")
def get_all_shop_clothes_info(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"clothes_info": shop_service.get_all_shop_clothes_info(username)}

@router.post("/clothes-info-by-filename")
def get_shop_clothes_info_by_filename(username: str = Form(...), filename: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")
    return {"clothes_info": shop_service.get_shop_clothes_info_by_filename(username, filename)}

@router.post("/clothes-filename")
def get_all_shop_clothes_filename(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"filename": shop_service.get_all_shop_clothes_filename(username)}