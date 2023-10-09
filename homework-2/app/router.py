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
    tags=["Recipes"]    
)


@router.get("/recipes", response_model=List[Recipe])
async def get_recipes():
    """
    Retrieve a list of all available recipes.
    
    Returns:
        List[Recipe]: A list containing all recipes.
    """

    return get_multiple_recipes()


@router.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    """
    Fetch a specific recipe by its ID.
    
    Args:
        recipe_id (int): The ID of the desired recipe.
        
    Raises:
        HTTPException: If the recipe with the provided ID is not found.
        
    Returns:
        Recipe: The requested recipe.
    """

    recipe = get_recipe_by_id(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: Recipe):
    """
    Create a new recipe.
    
    Args:
        recipe (Recipe): The new recipe object to be created.
        
    Returns:
        Recipe: The created recipe.
    """

    return add_recipe(recipe)


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    """
    Remove a specific recipe by its ID.
    
    Args:
        recipe_id (int): The ID of the recipe to be removed.
        
    Raises:
        HTTPException: If the recipe with the provided ID is not found.
        
    Returns:
        dict: A message indicating the success of the deletion and the deleted recipe.
    """

    deleted_recipe = remove_recipe(recipe_id)
    if deleted_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully", "recipe": deleted_recipe}


@router.post("/recipes/{recipe_id}/rate")
async def rate_recipe(recipe_id: int, rating: float):
    """
    Rate a specific recipe by its ID.
    
    Args:
        recipe_id (int): The ID of the recipe to be rated.
        rating (float): The rating value to be added to the recipe.
        
    Raises:
        HTTPException: 
            - If the rating is not between 0 and 5.0.
            - If the recipe with the provided ID is not found.
            
    Returns:
        Recipe: The rated recipe.
    """

    try:
        recipe = rate_recipe_by_id(recipe_id, rating)
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
