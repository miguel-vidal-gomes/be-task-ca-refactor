from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from .repository import ItemRepository
from be_task_ca.item.models.model import Item

""" SQL Repository """


class SQLItemRepository(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_item(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        return item

    def get_all_items(self) -> List[Item]:
        return self.db.query(Item).all()

    def find_item_by_name(self, name: str) -> Item:
        return self.db.query(Item).filter(Item.name == name).first()

    def find_item_by_id(self, id: UUID) -> Item:
        return self.db.query(Item).filter(Item.id == id).first()
