import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas import Recipe
from app.service import recipes_dict

clinet = TestClient(app)

def setup_recipes():
    """
    Clear the database and create default values
    """

    global recipes_dict
    recipes_dict.clear()
    recipes_dict.update({
        0: Recipe(name="Spaghetti Carbonara", description="A classic Italian pasta dish..."),
        1: Recipe(name="Chicken Curry", description="A fragrant Indian dish with spices, tomato, and chicken."),
        2: Recipe(name="Burger", description="An American classic with a beef patty, lettuce, and tomato in a bun."),
        3: Recipe(name="Fish Tacos", description="Mexican-inspired tacos with grilled fish and a tangy dressing."),
        4: Recipe(name="Chocolate Cake", description="A rich and moist dessert loved worldwide.")
    })

@pytest.mark.parametrize(
        "recipe_id, expected_result", 
        [(0, (200, recipes_dict[0])),
         (1, (200, recipes_dict[1])),
         (200, (404, {"detail": "Recipe not found"}))
         ]
)
def test_get_recipe(recipe_id, expected_result):
    """
    Test retrieving a recipe by its ID.
    
    Args:
        recipe_id (int): The ID of the recipe to retrieve.
        expected_result (tuple): A tuple containing the expected HTTP status
        and the expected recipe data.
        
    - Checks successful retrieval for valid IDs.
    - Ensures a 404 response for invalid IDs.
    """

    response = clinet.get(f"/recipes/{recipe_id}")
    assert response.status_code == expected_result[0]
    if response.status_code == 200:
        assert response.json() == vars(expected_result[1])
    else:
        assert response.json() == expected_result[1]

@pytest.mark.parametrize(
    "recipe, expected_result",
    [
        (
            {
                "name": "Pancake",
                "description": "Pancake",
                "rating": 4.0,
                "number_of_ratings": 1
            }, 
            (
                200, 
                {
                    "name": "Pancake",
                    "description": "Pancake",
                    "rating": 4,
                    "number_of_ratings": 1
                }
            )
        ),
        (
            {
             "name": "Dumplings",
             "description": "Meat and dough",
             "rating": 3.7,
             "number_of_ratings": 2
            }, 
            (
                200, 
                {
                    "name": "Dumplings",
                    "description": "Meat and dough",
                    "rating": 3.7,
                    "number_of_ratings": 2
                }
            )
        )
    ]
)
def test_create_recipe(recipe, expected_result):
    """
    Test creating a new recipe.
    
    Args:
        recipe (dict): The recipe data to be created.
        expected_result (tuple): A tuple containing the expected HTTP status and
        the expected recipe data after creation.
        
    - Validates successful creation with given inputs.
    - Checks the returned data against expected results.
    """

    setup_recipes()
    response = clinet.post(
        "/recipes/",
        json={"name": recipe["name"],
              "description": recipe["description"],
              "rating": recipe["rating"],
              "number_of_ratings": recipe["number_of_ratings"]
              }
    )
    assert response.status_code == expected_result[0]
    assert response.json() == expected_result[1]

@pytest.mark.parametrize(
        "recipe_id, rating, expected_result",
        [
            (
                0, 4.0, 
                (
                    200, 
                    {
                        "name": "Spaghetti Carbonara",
                        "description": "A classic Italian pasta dish with eggs, cheese, and bacon.",
                        "rating": 4.0,
                        "number_of_ratings": 1
                    }
                )
            ),
            (
                0, 5.0,
                (
                    200, 
                    {
                        "name": "Spaghetti Carbonara",
                        "description": "A classic Italian pasta dish with eggs, cheese, and bacon.",
                        "rating": 4.5,
                        "number_of_ratings": 2
                    }
                )
            ),
            (
                1, 239,
                (
                    400,
                    {
                    "detail": "Invalid rating value. Rating should be between 0 and 5.0"
                    }
                )
            )
        ]
)
def test_rate_a_recipe(recipe_id, rating, expected_result):
    """
    Test rating an existing recipe.
    
    Args:
        recipe_id (int): The ID of the recipe to rate.
        rating (float): The rating value to be added to the recipe.
        expected_result (tuple): A tuple containing the expected HTTP status and
        the expected recipe data after rating.
        
    - Evaluates successful rating for valid inputs.
    - Checks rating aggregation on repeated ratings for a recipe.
    - Ensures an error response for invalid rating values.
    """

    response = clinet.post(f"/recipes/{recipe_id}/rate", params={"rating": rating})
    print("Expected:", expected_result[1])
    print("Received:", response.json())
    assert response.status_code == expected_result[0]
    if "detail" in response.json():
        assert response.json() == expected_result[1]
    else:
        assert response.json()["rating"] == expected_result[1]["rating"]
    