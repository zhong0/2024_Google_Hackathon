from fastapi import APIRouter
from .ClothesApi import router as clothes_router
from .RecommendApi import router as recommend_router
from .AuthApi import router as auth_router
from .UploadApi import router as upload_router

api_router = APIRouter()
api_router.include_router(clothes_router, prefix="/clothes", tags=["Clothes"])
api_router.include_router(recommend_router, prefix="/recommend", tags=["Recommend"])
api_router.include_router(upload_router, prefix="/upload", tags=["Upload"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authorization"])