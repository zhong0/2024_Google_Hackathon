from fastapi import APIRouter, HTTPException, Form, status, Query
from ..service.RecommendService import RecommendService
from ..entity.RecommendRequest import RecommendRequest
from ..entity.ExploreRequest import ExploreRequest
#from ..entity.ExplorePiecesRequest import ExplorePiecesRequest
from ..utils import Const as const
import json

router = APIRouter()
service = RecommendService()

@router.post("/recommend-by-text")
def recommend_by_text(request: RecommendRequest):
    return service.recommend_from_wardrobe(
        username=request.username,
        style=request.style,
        occasion=request.occasion,
        specific_clothes=request.specific_clothes,
        isRefresh=request.isRefresh)

@router.post("/explore-outfit")
def explore_outfit(request: ExploreRequest):
    return service.explore_outfit(
        request.username,
        request.style,
        const.explore_outfit_number
    )
'''
@router.post("/explore-pieces-recommendation")
def explore_outfit(request: ExplorePiecesRequest):
    return service.explore_pieces_recommendation(
        request.username,
        request.style,
        request.specific_clothes,
        const.explore_outfit_number
    )'''

@router.post("/create", deprecated=True)
def create_history_recommend(username: str = Form(...), recommend_set: str = Form(...)):
    try:
        recommend_data = json.loads(recommend_set)
        if service.create_history_recommend(username, recommend_data):
            return {"message": "Recommendation created successfully"}
        else :
            return {"message": "Recommendation created failed"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/insert", deprecated=True)
def insert_history_recommend(username: str = Form(...), recommend_set: str = Form(...)):
    try:
        recommend_data = json.loads(recommend_set)
        if service.insert_history_recommend(username, recommend_data):
            return {"message": "Recommendation inserted successfully"}
        else :
            return {"message": "Recommendation inserted failed"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/remove", deprecated=True)
def remove_history_recommend(username: str = Form(...)):
    try:
        if service.remove_history_recommend(username):
            return {"message": "Recommendation removed successfully"}
        else :
            return {"message": "Recommendation inseremovedrted failed"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
