from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from be_task_ca.user.models.model import User

""" 

This is an abstract base class to make repository operations fully independent of the persistence implementation. 
This allows seamless substitution of the persistent repository methodology from the original SQL
with an in-memory implementation (or any other methodology).

"""


class UserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def find_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def find_user_by_id(self, id: UUID) -> User:
        pass

    @abstractmethod
    def find_cart_items_for_user_id(user_id, db):
        pass
