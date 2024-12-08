from fastapi.testclient import TestClient
from fastapi import FastAPI
from be_task_ca.item.interface.api import item_router

app = FastAPI()
app.include_router(item_router)

client = TestClient(app)


def test_post_item():
    """tests that an item can be created via the API"""
    response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "Test Desc",
            "price": 10.5,
            "quantity": 100,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"


def test_get_items():
    """tests that the listing api returns a recently created item"""
    client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "Test Desc",
            "price": 10.5,
            "quantity": 100,
        },
    )
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_post_item_missing_fields():
    """tests that an item cannot be created with missing fields"""
    response = client.post(
        "/items/",
        json={
            "name": "Incomplete Item",  # Missing price, quantity, etc.
        },
    )
    assert response.status_code == 422


def test_post_item_invalid_types():
    """tests that an item cannot be created with invalid types"""
    response = client.post(
        "/items/",
        json={
            "name": "Invalid Item",
            "description": "Some Desc",
            "price": "invalid_price",  # Should be a float
            "quantity": "invalid_quantity",  # Should be an int
        },
    )
    assert response.status_code == 422
