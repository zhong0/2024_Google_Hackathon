from pydantic import BaseModel
from typing import List, Optional

class ExploreRequest(BaseModel):
    username: str 
    style: Optional[List[str]] = None
    specific_clothes_filename: str
    recommend_count: int
