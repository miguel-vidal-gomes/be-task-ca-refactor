import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from uuid import uuid4
from be_task_ca.user.interface.api import user_router
from be_task_ca.user.repositories.in_memory_repository import InMemoryUserRepository

app = FastAPI()
app.include_router(user_router)

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_in_memory_repository():
    InMemoryUserRepository.clear_storage()


def test_post_user():
    """Tests that a user can be created via the API."""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": "hashedpassword123",
            "shipping_address": "123 Main St",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"


def test_get_specific_user():
    """Tests that the retrieval API returns a recently created user."""
    user_create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": "hashedpassword123",
            "shipping_address": "123 Main St",
        },
    )
    user_id = user_create_response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["first_name"] == "Test"
    assert response.json()["last_name"] == "User"


def test_post_user_missing_fields():
    """Tests that a user cannot be created with missing fields."""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",  # Missing first_name, last_name, etc.
        },
    )
    assert response.status_code == 422


def test_post_user_invalid_types():
    """Tests that a user cannot be created with invalid types."""
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": 12345,  # Should be a string
            "shipping_address": True,  # Should be a string
        },
    )
    assert response.status_code == 422


def test_add_item_to_cart():
    """Tests that an item can be added to the user's cart."""
    user_create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": "hashedpassword123",
            "shipping_address": "123 Main St",
        },
    )
    user_id = user_create_response.json()["id"]
    item_id = str(uuid4())  # Mock item ID
    response = client.post(
        f"/users/{user_id}/cart",
        json={
            "item_id": item_id,
            "quantity": 2,
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Item added to cart successfully"


def test_list_items_in_cart():
    """Tests that items in the user's cart can be listed."""
    user_create_response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "hashed_password": "hashedpassword123",
            "shipping_address": "123 Main St",
        },
    )
    user_id = user_create_response.json()["id"]
    item_id = str(uuid4())  # Mock item ID
    client.post(
        f"/users/{user_id}/cart",
        json={
            "item_id": item_id,
            "quantity": 2,
        },
    )
    response = client.get(f"/users/{user_id}/cart")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["item_id"] == item_id
    assert response.json()[0]["quantity"] == 2
