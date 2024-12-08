from uuid import UUID
from typing import List, Optional
from .model import User as DomainUser, CartItem as DomainCartItem


class InMemoryCartItem:
    def __init__(self, user_id: UUID, item_id: UUID, quantity: int):
        self.user_id = user_id
        self.item_id = item_id
        self.quantity = quantity

    def to_domain(self) -> DomainCartItem:
        """Convert the InMemoryCartItem to the universal CartItem model."""
        return DomainCartItem(
            user_id=self.user_id,
            item_id=self.item_id,
            quantity=self.quantity,
        )

    @staticmethod
    def from_domain(domain_cart_item: DomainCartItem) -> "InMemoryCartItem":
        """Convert a universal CartItem model to InMemoryCartItem."""
        return InMemoryCartItem(
            user_id=domain_cart_item.user_id,
            item_id=domain_cart_item.item_id,
            quantity=domain_cart_item.quantity,
        )


class InMemoryUser:
    def __init__(
        self,
        id: UUID,
        email: str,
        first_name: str,
        last_name: str,
        hashed_password: str,
        shipping_address: Optional[str] = None,
        cart_items: Optional[List[InMemoryCartItem]] = None,
    ):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.shipping_address = shipping_address
        self.cart_items = cart_items or []

    def to_domain(self) -> DomainUser:
        """Convert the InMemoryUser to the universal User model."""
        return DomainUser(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=self.hashed_password,
            shipping_address=self.shipping_address,
            cart_items=[item.to_domain() for item in self.cart_items],
        )

    @staticmethod
    def from_domain(domain_user: DomainUser) -> "InMemoryUser":
        """Convert a universal User model to InMemoryUser."""
        return InMemoryUser(
            id=domain_user.id,
            email=domain_user.email,
            first_name=domain_user.first_name,
            last_name=domain_user.last_name,
            hashed_password=domain_user.hashed_password,
            shipping_address=domain_user.shipping_address,
            cart_items=[
                InMemoryCartItem.from_domain(item) for item in domain_user.cart_items
            ],
        )
