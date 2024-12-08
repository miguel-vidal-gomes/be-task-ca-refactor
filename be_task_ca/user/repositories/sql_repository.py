from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from .repository import UserRepository
from be_task_ca.user.models.model import User, CartItem

""" SQL Repository """


class SQLUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        return user

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def find_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def find_user_by_id(self, id: UUID) -> User:
        return self.db.query(User).filter(User.id == id).first()

    def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.user_id == user_id).all()
