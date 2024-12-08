from fastapi import HTTPException
from uuid import UUID, uuid4  # Import UUID generator
from .repositories.repository import UserRepository
from be_task_ca.user.models.model import User, CartItem
from be_task_ca.user.interface.schema import (
    CreateUserRequest,
    CreateUserResponse,
    AddToCartRequest,
)


class UserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: CreateUserRequest) -> CreateUserResponse:
        # Check if the user already exists by email
        similar_user = self.repository.find_user_by_email(user.email)
        if similar_user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )

        new_user = User(
            id=uuid4(),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            hashed_password=user.hashed_password,
            shipping_address=user.shipping_address,
        )
        self.repository.save_user(new_user)
        return CreateUserResponse(
            id=new_user.id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            shipping_address=new_user.shipping_address,
        )

    def find_user_by_id(self, user_id: UUID) -> CreateUserResponse:
        # Fetch a user by their ID
        user = self.repository.find_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return CreateUserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            shipping_address=user.shipping_address,
        )

    def add_item_to_cart(self, user_id: UUID, cart_item: AddToCartRequest):
        # Add an item to the user's cart
        user = self.repository.find_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        new_cart_item = CartItem(
            user_id=user_id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
        )
        self.repository.add_cart_item(new_cart_item)
        return {"message": "Item added to cart successfully"}

    def list_items_in_cart(self, user_id: UUID):
        # List all items in the user's cart
        cart_items = self.repository.find_cart_items_for_user_id(user_id)
        if not cart_items:
            raise HTTPException(
                status_code=404, detail="Cart is empty or user not found"
            )
        return cart_items
