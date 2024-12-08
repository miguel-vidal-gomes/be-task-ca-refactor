from fastapi import APIRouter, Depends

from be_task_ca.item.repositories.repository import ItemRepository
from sqlalchemy.orm import Session
from be_task_ca.item.usecases import ItemUseCase
from be_task_ca.item.repositories.in_memory_repository import (
    InMemoryItemRepository,
)  # Default repository
from be_task_ca.item.repositories.sql_repository import (
    SQLItemRepository,
)  # Optional SQL repository
from .schema import CreateItemRequest, CreateItemResponse, AllItemsResponse
from be_task_ca.database import get_db

"""

The API can run without requiring any external dependencies (e.g., a database).
Switching back to a SQL-based repository or another implementation is still simple, 
as the API interacts only with the ItemRepository interface.

"""


def get_repository(
    repo_type: str = "memory", db: Session = Depends(get_db)
) -> ItemRepository:
    if repo_type == "memory":
        return InMemoryItemRepository()
    elif repo_type == "sql":
        return SQLItemRepository(db=db)
    raise ValueError(f"Unknown repository type: {repo_type}")


# Dependency to provide an ItemUseCase with the dynamically selected repository
def get_item_use_case(
    repository: ItemRepository = Depends(get_repository),
) -> ItemUseCase:
    return ItemUseCase(repository)


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/", response_model=CreateItemResponse)
async def post_item(
    item: CreateItemRequest,
    item_use_case: ItemUseCase = Depends(get_item_use_case),
) -> CreateItemResponse:
    return item_use_case.create_item(item)


@item_router.get("/", response_model=AllItemsResponse)
async def get_items(item_use_case: ItemUseCase = Depends(get_item_use_case)):
    return AllItemsResponse(items=item_use_case.get_all_items())
