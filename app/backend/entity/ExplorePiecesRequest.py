from pydantic import BaseModel
from typing import List, Optional

class ExplorePiecesRequest(BaseModel):
    username: str 
    style: Optional[List[str]] = None
    specific_clothes: Optional[List[str]] = None
    recommend_count: int