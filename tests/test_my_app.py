from fastapi.testclient import TestClient
from my_app.recipes_main import app

client = TestClient(app)


def test_create_item():
    test_request = {"recipe_name": "Test recipe",
                    "cooking_time": 10,
                    "ingredients": "test, test, test",
                    "description": "some test description"}
    response = client.post(
        "/recipes/",
        json=test_request,
    )
    assert response.status_code == 200
    assert response.json() == test_request


def test_read_main():
    response = client.get('/recipes/')
    assert response.status_code == 200
    assert response.json() is not None


def test_read_nonexistent_item():
    response = client.get('/recipes/123456789')
    assert response.status_code == 404
    assert response.json() == {"detail": "Recipe not found"}

