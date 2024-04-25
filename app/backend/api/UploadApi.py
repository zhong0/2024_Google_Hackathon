from fastapi import FastAPI, Response, File, UploadFile, APIRouter, HTTPException, Form
from fastapi.responses import JSONResponse
from ..service.UploadService import UploadService
from typing import List

router = APIRouter()
service = UploadService()


@router.post("/upload-images", status_code=200)
async def upload_images(response:Response, username: str, files: List[UploadFile]=File(...)):
    #check if image type
    allowed_extension = ["jpg", "jpeg"]
    for f in files:
        if not f.content_type.startswith("image/"):
            return JSONResponse(status_code=400, content={"error": "only support image uplaoding."})
        if f.filename.split(".")[-1] not in allowed_extension:
            return JSONResponse(status_code=400, content={"error": "only support image extension \".jpg\", \".jpeg\""})
    result = await service.upload_images(username, files)
    return result
