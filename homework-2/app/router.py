from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import Recipe
from app.service import (
    add_recipe,
    get_multiple_recipes,
    get_recipe_by_id,
    rate_recipe_by_id,
    remove_recipe,
)

router = APIRouter(
    tags=["Recipe"]    
)


@router.get("/recipes", response_model=List[Recipe])
async def get_recipes():
    return get_multiple_recipes()


@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    recipe = get_recipe_by_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: Recipe):
    return add_recipe(recipe)


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    deleted_recipe = remove_recipe(recipe_id)
    if deleted_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully", "recipe": deleted_recipe}


@router.post("/recipes/{recipe_id}/rate")
async def rate_recipe(recipe_id: int, rating: float):
    try:
        recipe = rate_recipe_by_id(recipe_id, rating)
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
