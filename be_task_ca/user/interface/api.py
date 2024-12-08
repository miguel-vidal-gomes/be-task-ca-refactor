from fastapi import APIRouter, Depends
from uuid import UUID

from be_task_ca.user.repositories.repository import UserRepository
from sqlalchemy.orm import Session
from be_task_ca.user.usecases import UserUseCase
from be_task_ca.user.repositories.in_memory_repository import (
    InMemoryUserRepository,
)  # Default repository
from be_task_ca.user.repositories.sql_repository import (
    SQLUserRepository,
)  # Optional SQL repository
from be_task_ca.user.interface.schema import (
    CreateUserRequest,
    CreateUserResponse,
    AddToCartRequest,
)
from be_task_ca.database import get_db

"""

The API can run without requiring any external dependencies (e.g., a database).
Switching back to a SQL-based repository or another implementation is still simple, 
as the API interacts only with the UserRepository interface.

"""


def get_repository(
    repo_type: str = "memory", db: Session = Depends(get_db)
) -> UserRepository:
    if repo_type == "memory":
        return InMemoryUserRepository()
    elif repo_type == "sql":
        return SQLUserRepository(db=db)
    raise ValueError(f"Unknown repository type: {repo_type}")


# Dependency to provide an UserUseCase with the dynamically selected repository
def get_user_use_case(
    repository: UserRepository = Depends(get_repository),
) -> UserUseCase:
    return UserUseCase(repository)


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/", response_model=CreateUserResponse)
async def post_user(
    user: CreateUserRequest,
    user_use_case: UserUseCase = Depends(get_user_use_case),
) -> CreateUserResponse:
    return user_use_case.create_user(user)


@user_router.get("/{user_id}", response_model=CreateUserResponse)
async def get_user(
    user_id: UUID, user_use_case: UserUseCase = Depends(get_user_use_case)
) -> CreateUserResponse:
    return user_use_case.find_user_by_id(user_id)


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID,
    cart_item: AddToCartRequest,
    user_use_case: UserUseCase = Depends(get_user_use_case),
):
    return user_use_case.add_item_to_cart(user_id, cart_item)


@user_router.get("/{user_id}/cart")
async def get_cart(
    user_id: UUID, user_use_case: UserUseCase = Depends(get_user_use_case)
):
    return user_use_case.list_items_in_cart(user_id)
