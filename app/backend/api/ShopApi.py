from fastapi import APIRouter, HTTPException, Form
from ..service.ShopService import ShopService
from ..entity.SaleClothesRequest import SaleClothesRequest


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

@router.post("/clothes-sale-info-by-filename")
def get_clothes_sale_info_by_filename(username:str = Form(...), filename: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    return shop_service.get_clothes_sale_info_by_filename(username, filename)

@router.post("/clothes-on-sale")
def clothes_on_sale(request: SaleClothesRequest):
    if request.username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if request.filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")
    if request.price is None: 
        raise HTTPException(status_code=400, detail="Price is required")
    
    if shop_service.clothes_on_sale(
        request.username, request.filename, request.brand, request.size, request.price, request.owner_description):
        return {"message": "Display clothes on sale successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to sale")

@router.post("/remove-clothes-from-shop")
def remove_clothes_from_shop(username: str = Form(...), filename: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")
    
    if shop_service.remove_clothes_from_shop(username, filename):
        return {"message": "Remove clothes from sale successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to remove from shop")

@router.post("/update-sale-info")
def clothes_on_sale(request: SaleClothesRequest):
    if request.username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if request.filename is None:
        raise HTTPException(status_code=400, detail="Filename is required")
    if request.price is None: 
        raise HTTPException(status_code=400, detail="Price is required")
    
    if shop_service.update_sale_info(
        request.username, request.filename, request.brand, request.size, request.price, request.owner_description):
        return {"message": "update sale of clothes successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to sale")

@router.post("/file-path-group-by-category")
def get_file_path_group_by_category(username: str = Form(...)):
    if username is None :
        raise HTTPException(status_code=400, detail="Username is required")
    return {"file_path": shop_service.get_file_path_group_by_category(username)}


@router.post("/get-all-user-filename")
def get_all_user_filename():
    return {"filename": shop_service.get_all_user_filename()}

