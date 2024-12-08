from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from be_task_ca.item.models.model import Item

""" 

This is an abstract base class to make repository operations fully independent of the persistence implementation. 
This allows seamless substitution of the persistent repository methodology from the original SQL
with an in-memory implementation (or any other methodology).

"""


class ItemRepository(ABC):
    @abstractmethod
    def save_item(self, item: Item) -> Item:
        pass

    @abstractmethod
    def get_all_items(self) -> List[Item]:
        pass

    @abstractmethod
    def find_item_by_name(self, name: str) -> Item:
        pass

    @abstractmethod
    def find_item_by_id(self, id: UUID) -> Item:
        pass
