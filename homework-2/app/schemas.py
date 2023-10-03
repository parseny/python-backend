from typing import List, Optional

from pydantic import BaseModel


class Recipe(BaseModel):
    """
    Recipe class to store recipe information
    """

    name: str
    description: str
    rating: Optional[float] = 0.0
    number_of_ratings: int = 0
