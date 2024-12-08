from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from be_task_ca.database import Base
from be_task_ca.user.models.model import User as DomainUser, CartItem as DomainCartItem


class SQLAlchemyCartItem(Base):
    __tablename__ = "cart_items"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    item_id: Mapped[UUID] = mapped_column(ForeignKey("items.id"), primary_key=True)
    quantity: Mapped[int]

    def to_domain(self) -> DomainCartItem:
        """Convert the SQLAlchemyCartItem to the universal CartItem model."""
        return DomainCartItem(
            user_id=self.user_id,
            item_id=self.item_id,
            quantity=self.quantity,
        )

    @staticmethod
    def from_domain(domain_cart_item: DomainCartItem) -> "SQLAlchemyCartItem":
        """Convert a universal CartItem model to SQLAlchemyCartItem."""
        return SQLAlchemyCartItem(
            user_id=domain_cart_item.user_id,
            item_id=domain_cart_item.item_id,
            quantity=domain_cart_item.quantity,
        )


class SQLAlchemyUser(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    shipping_address: Mapped[str] = mapped_column(default=None)
    cart_items: Mapped[list["SQLAlchemyCartItem"]] = relationship(
        "SQLAlchemyCartItem", backref="user"
    )

    def to_domain(self) -> DomainUser:
        """Convert the SQLAlchemyUser to the universal User model."""
        return DomainUser(
            id=self.id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            hashed_password=self.hashed_password,
            shipping_address=self.shipping_address,
            cart_items=[cart_item.to_domain() for cart_item in self.cart_items],
        )

    @staticmethod
    def from_domain(domain_user: DomainUser) -> "SQLAlchemyUser":
        """Convert a universal User model to SQLAlchemyUser."""
        return SQLAlchemyUser(
            id=domain_user.id,
            email=domain_user.email,
            first_name=domain_user.first_name,
            last_name=domain_user.last_name,
            hashed_password=domain_user.hashed_password,
            shipping_address=domain_user.shipping_address,
            cart_items=[
                SQLAlchemyCartItem.from_domain(ci) for ci in domain_user.cart_items
            ],
        )
