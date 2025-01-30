from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/recipes",
        json={
            "title": "Тестовый рецепт",
            "cooking_time": 30,
            "ingredients": "Ингредиент 1, Ингредиент 2",
            "description": "Описание тестового рецепта",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Тестовый рецепт"
    assert data["views"] == 0
    assert "id" in data


def test_get_recipes():
    response = client.get("/recipes")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)


def test_get_recipe():
    create_response = client.post(
        "/recipes",
        json={
            "title": "Тестовый рецепт",
            "cooking_time": 30,
            "ingredients": "Ингредиент 1, Ингредиент 2",
            "description": "Описание тестового рецепта",
        },
    )

    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == recipe_id
