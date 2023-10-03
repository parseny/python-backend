from typing import List, Optional

from pydantic import BaseModel


class Recipe(BaseModel):
    name: str
    description: str
    rating: Optional[float] = 0.0
    number_of_ratings: int = 0
