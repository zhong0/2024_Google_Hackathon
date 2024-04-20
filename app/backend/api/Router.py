from fastapi import APIRouter
from .ClothesApi import router as clothes_router
from .RecommendApi import router as recommend_router

api_router = APIRouter()
api_router.include_router(clothes_router, prefix="/clothes", tags=["clothes"])
api_router.include_router(recommend_router, prefix="/recommend", tags=["recommend"])