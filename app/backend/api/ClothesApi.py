from fastapi import APIRouter, HTTPException, Form
from ..service.ClothService import ClothesService

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

@router.post("/file-path-group-by-category")
def get_file_path_group_by_category(username: str = Form(...)):
    if username is None :
        raise HTTPException(status_code=400, detail="Username is required")
    return {"file_path": service.get_file_path_group_by_category(username)}

@router.post("/style-by-filename")
def get_style_by_filename(username: str = Form(...), filename: str = Form(...)):
    if username is None or filename is None:
        raise HTTPException(status_code=400, detail="Username & filename is required")
    return {"style": service.get_style_by_filename(username, filename)}

@router.post("/favorite-set")
def get_favorite_set(username: str = Form(...)):
    if username is None :
        raise HTTPException(status_code=400, detail="Username is required")
    return {"favorite_set": service.get_favorite_set(username)}

@router.post("/clothes-info", deprecated=True)
def get_all_clothes_info(username: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    return {"clothes_info": service.get_all_clothes_info(username)}

@router.post("/add-favorite-set")
def insert_favorite_set(username: str = Form(...), filename_list:list[str] = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename_list is None:
        raise HTTPException(status_code=400, detail="Filenames is required")
    return service.insert_favorite_set(username, filename_list)

@router.post("/remove-favorite-set")
def remove_favorite_set(username: str = Form(...), filename_list:list[str] = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename_list is None:
        raise HTTPException(status_code=400, detail="Filenames is required")
    return service.remove_favorite_set(username, filename_list)

@router.post("/remove-clothes-from-wardrobe")
def remove_clothes(username: str = Form(...), filename: str = Form(...)):
    if username is None:
        raise HTTPException(status_code=400, detail="Username is required")
    if filename is None:
        raise HTTPException(status_code=400, detail="Filenames is required")
    
    if service.remove_clothes_from_wardrobe(username, filename):
        return {"message": "Remove clothes from wardrobe successfully"}
    
    raise HTTPException(status_code=500, detail="Failed to remove clothes from wardrobe")