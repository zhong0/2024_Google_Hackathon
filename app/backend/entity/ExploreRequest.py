from pydantic import BaseModel
from typing import List, Optional

class ExploreRequest(BaseModel):
    username: str 
    style: str
    recommend_count: int