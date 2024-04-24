from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    username: str 
    style: Optional[List[str]] = None
    occasion: Optional[List[str]] = None
    specific_clothes: Optional[List[str]] = None
    isRefresh: bool = False
