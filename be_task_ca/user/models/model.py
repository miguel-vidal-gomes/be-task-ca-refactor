from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class CartItem:
    user_id: UUID
    item_id: UUID
    quantity: int

    @staticmethod
    def create(user_id: UUID, item_id: UUID, quantity: int) -> "CartItem":
        """Factory method to create a new CartItem."""
        return CartItem(
            user_id=user_id,
            item_id=item_id,
            quantity=quantity,
        )


@dataclass
class User:
    id: UUID
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str] = None
    cart_items: List[CartItem] = field(default_factory=list)

    @staticmethod
    def create(
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
        shipping_address: Optional[str] = None,
    ) -> "User":
        """Factory method to create a new User with a unique ID."""
        return User(
            id=uuid4(),
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            shipping_address=shipping_address,
        )
