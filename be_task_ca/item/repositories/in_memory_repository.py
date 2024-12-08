from .repository import ItemRepository
from be_task_ca.item.models.model import Item
from typing import List
from uuid import UUID, uuid4

""" In-Memory Repository """


class InMemoryItemRepository(ItemRepository):
    _storage = {}  # Shared class-level dictionary for persistence

    def save_item(self, item: Item) -> Item:
        if not item.id:  # If the item doesn't have an ID, assign one
            item.id = uuid4()
        self._storage[item.id] = item
        return item

    def find_item_by_name(self, name: str) -> Item | None:
        for item in self._storage.values():
            if item.name == name:
                return item
        return None

    def find_item_by_id(self, id: UUID) -> Item | None:
        return self._storage.get(id)

    def get_all_items(self) -> List[Item]:
        return list(self._storage.values())
