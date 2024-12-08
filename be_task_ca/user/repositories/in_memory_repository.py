from .repository import UserRepository
from be_task_ca.user.models.model import User, CartItem
from typing import List, Dict
from uuid import UUID, uuid4

""" In-Memory Repository """


class InMemoryUserRepository(UserRepository):
    _users: Dict[UUID, User] = {}
    _cart_items: Dict[UUID, List[CartItem]] = {}

    @classmethod
    def clear_storage(cls):
        cls._users.clear()
        cls._cart_items.clear()

    def save_user(self, user: User) -> User:
        if not user.id:  # Assign an ID if missing
            user.id = uuid4()
        self._users[user.id] = user
        return user

    def find_user_by_id(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    def find_user_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> List[User]:
        return list(self._users.values())

    def add_cart_item(self, cart_item: CartItem):
        if cart_item.user_id not in self._users:
            raise ValueError("User not found")

        if cart_item.user_id not in self._cart_items:
            self._cart_items[cart_item.user_id] = []

        # Add or update cart item
        existing_item = next(
            (
                item
                for item in self._cart_items[cart_item.user_id]
                if item.item_id == cart_item.item_id
            ),
            None,
        )
        if existing_item:
            existing_item.quantity += cart_item.quantity
        else:
            self._cart_items[cart_item.user_id].append(cart_item)

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        return self._cart_items.get(user_id, [])
