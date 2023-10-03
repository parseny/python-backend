import pytest

from app.schemas import Recipe
from app.service import (
    add_recipe,
    get_multiple_recipes,
    get_recipe_by_id,
    rate_recipe_by_id,
    recipes_dict,
    remove_recipe,
)


def setup_recipes():
    global recipes_dict
    recipes_dict.clear()
    recipes_dict.update({
        0: Recipe(name="Spaghetti Carbonara", description="A classic Italian pasta dish..."),
        1: Recipe(name="Chicken Curry", description="A fragrant Indian dish with spices, tomato, and chicken."),
        2: Recipe(name="Burger", description="An American classic with a beef patty, lettuce, and tomato in a bun."),
        3: Recipe(name="Fish Tacos", description="Mexican-inspired tacos with grilled fish and a tangy dressing."),
        4: Recipe(name="Chocolate Cake", description="A rich and moist dessert loved worldwide.")
    })
    global next_id
    next_id = 5
    return recipes_dict


def clear_recipes():
    global recipes_dict
    recipes_dict.clear()
    global next_id
    next_id = 0


def test_get_recipes():
    setup_recipes()
    assert len(get_multiple_recipes()) == 5


@pytest.mark.parametrize("name, description, expected_len", [("test", "test desc", 6)])
def test_add_recipe(name, description, expected_len):
    """
    Test if a new recipe can be added.
    
    Args:
    - name: The name of the recipe.
    - description: The description of the recipe.
    - expected_len: The expected number of recipes after adding.
    """

    r = Recipe(name=name, description=description)
    add_recipe(r)
    assert len(get_multiple_recipes()) == expected_len
    assert get_multiple_recipes()[expected_len - 1].name == name
    assert get_multiple_recipes()[expected_len - 1].description == description
    assert not (remove_recipe(expected_len - 1) is None)


@pytest.mark.parametrize(
    "recipe_id, rating, expected_rating, expected_number_of_ratings",
    [(0, 5, 5, 1), (1, 4, 4, 1), (2, 3, 3, 1), (3, 2, 2, 1), (4, 1, 1, 1)]
)
def test_rate_recipe(recipe_id, rating, expected_rating, expected_number_of_ratings):
    """
    Test if the recipe can be rated.
    
    Args:
    - recipe_id: The id of the recipe to be rated.
    - rating: The rating given to the recipe.
    - expected_rating: The expected average rating after the new rating.
    - expected_number_of_ratings: The expected total number of ratings after the new rating.
    """

    setup_recipes()
    recipe = rate_recipe_by_id(recipe_id, rating)
    assert recipe.rating == expected_rating
    assert recipe.number_of_ratings == expected_number_of_ratings


@pytest.mark.parametrize(
    "ratings,expected_avg",
    [
        ([3.0, 5.0], 4.0),
        ([1.0, 2.0, 3.0], 2.0),
        ([5.0, 5.0], 5.0),
    ],
)
def test_rate_recipe_multiple_times(ratings, expected_avg):
    """
    Test if a recipe can be rated multiple times and calculates average correctly.
    
    Args:
    - ratings: A list of ratings given to the recipe.
    - expected_avg: The expected average rating after all ratings.
    """

    setup_recipes()
    for rating in ratings:
        rate_recipe_by_id(0, rating)
    updated_recipe = get_recipe_by_id(0)
    assert updated_recipe.rating == expected_avg


@pytest.mark.parametrize(
    "recipe_id, expected_recipe",
    [
        (0, Recipe(name="Spaghetti Carbonara", description="A classic Italian pasta dish with eggs, cheese, and bacon.")),
        (1, Recipe(name="Chicken Curry", description="A fragrant Indian dish with spices, tomato, and chicken.")),
        (2, Recipe(name="Burger", description="An American classic with a beef patty, lettuce, and tomato in a bun.")),
        (3, Recipe(name="Fish Tacos", description="Mexican-inspired tacos with grilled fish and a tangy dressing.")),
        (4, Recipe(name="Chocolate Cake", description="A rich and moist dessert loved worldwide."))
    ]
)
def delete_by_id(recipe_id, expected_recipe):
    """
    Test if a recipe can be deleted by its ID.
    
    Args:
    - recipe_id: The id of the recipe to be deleted.
    - expected_recipe: The expected details of the deleted recipe.
    """

    setup_recipes()
    deleted_recipe = delete_by_id(recipe_id)
    assert deleted_recipe == expected_recipe
