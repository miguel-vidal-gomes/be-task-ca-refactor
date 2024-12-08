from uuid import UUID
from .model import Item as DomainItem


class InMemoryItem:
    def __init__(
        self, id: UUID, name: str, description: str, price: float, quantity: int
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def to_domain(self) -> DomainItem:
        """Convert the InMemoryItem to the universal Item model."""
        return DomainItem(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
        )

    @staticmethod
    def from_domain(domain_item: DomainItem) -> "InMemoryItem":
        """Convert a universal Item model to InMemoryItem."""
        return InMemoryItem(
            id=domain_item.id,
            name=domain_item.name,
            description=domain_item.description,
            price=domain_item.price,
            quantity=domain_item.quantity,
        )
