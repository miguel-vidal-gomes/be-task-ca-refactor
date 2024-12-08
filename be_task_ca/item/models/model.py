from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Item:
    id: UUID
    name: str
    description: str
    price: float
    quantity: int

    @staticmethod
    def create(name: str, description: str, price: float, quantity: int) -> "Item":
        """Factory method to create a new Item with a unique ID."""
        return Item(
            id=uuid4(),
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )
