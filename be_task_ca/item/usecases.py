from fastapi import HTTPException
from uuid import uuid4  # Import UUID generator
from .repositories.repository import ItemRepository
from .models.model import Item
from be_task_ca.item.interface.schema import CreateItemRequest, CreateItemResponse


class ItemUseCase:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(self, item: CreateItemRequest) -> CreateItemResponse:
        # Check if the item already exists by name
        similar_item = self.repository.find_item_by_name(item.name)
        if similar_item:
            raise HTTPException(
                status_code=400, detail="Item with this name already exists"
            )

        new_item = Item(
            id=uuid4(),
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        self.repository.save_item(new_item)
        return CreateItemResponse(
            id=new_item.id,
            name=new_item.name,
            description=new_item.description,
            price=new_item.price,
            quantity=new_item.quantity,
        )

    def get_all_items(self) -> list[CreateItemResponse]:
        items = self.repository.get_all_items()
        return [
            CreateItemResponse(
                id=item.id,
                name=item.name,
                description=item.description,
                price=item.price,
                quantity=item.quantity,
            )
            for item in items
        ]
