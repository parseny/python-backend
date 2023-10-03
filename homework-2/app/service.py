from typing import Dict, List, Optional

from app.schemas import Recipe

recipes_dict: Dict[int, Recipe] = {
    0: Recipe(name="Spaghetti Carbonara", description="A classic Italian pasta dish with eggs, cheese, and bacon."),
    1: Recipe(name="Chicken Curry", description="A fragrant Indian dish with spices, tomato, and chicken."),
    2: Recipe(name="Burger", description="An American classic with a beef patty, lettuce, and tomato in a bun."),
    3: Recipe(name="Fish Tacos", description="Mexican-inspired tacos with grilled fish and a tangy dressing."),
    4: Recipe(name="Chocolate Cake", description="A rich and moist dessert loved worldwide.")
}
next_id = 5

def get_multiple_recipes() -> List[Recipe]:
    return list(recipes_dict.values())


def get_recipe_by_id(recipe_id: int) -> Recipe:
    return recipes_dict.get(recipe_id)


def add_recipe(recipe: Recipe) -> Recipe:
    global next_id
    recipes_dict[next_id] = recipe
    next_id += 1
    return recipe


def rate_recipe_by_id(recipe_id: int, rating: float) -> Optional[Recipe]:
    if not (0 < rating <= 5.0):
        raise ValueError("Invalid rating value. Rating should be between 0 and 5.0")
    recipe = recipes_dict.get(recipe_id)
    if recipe:
        total = recipe.rating * recipe.number_of_ratings + rating
        recipe.number_of_ratings += 1
        recipe.rating = total / recipe.number_of_ratings
        return recipe
    return None


def remove_recipe(recipe_id: int) -> Optional[Recipe]:
    return recipes_dict.pop(recipe_id, None)
