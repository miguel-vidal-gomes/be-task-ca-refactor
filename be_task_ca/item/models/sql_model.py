from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from be_task_ca.database import Base
from .model import Item as DomainItem


class SQLAlchemyItem(Base):
    __tablename__ = "items"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int]

    def to_domain(self) -> DomainItem:
        """Convert the SQLAlchemyItem to the universal Item model."""
        return DomainItem(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=self.quantity,
        )

    @staticmethod
    def from_domain(domain_item: DomainItem) -> "SQLAlchemyItem":
        """Convert a universal Item model to SQLAlchemyItem."""
        return SQLAlchemyItem(
            id=domain_item.id,
            name=domain_item.name,
            description=domain_item.description,
            price=domain_item.price,
            quantity=domain_item.quantity,
        )
