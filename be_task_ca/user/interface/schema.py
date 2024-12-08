from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator


class CreateUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: Optional[str] = Field(default=None)

    @validator("hashed_password")
    def validate_hashed_password(cls, value):
        if not isinstance(value, str):
            raise ValueError("hashed_password must be a string")
        return value

    @validator("shipping_address", pre=True, always=True)
    def validate_shipping_address(cls, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("shipping_address must be a string or null")
        return value

    class Config:
        anystr_strip_whitespace = True


class CreateUserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    shipping_address: Optional[str] = None


class AddToCartRequest(BaseModel):
    item_id: UUID
    quantity: int


class CartItemResponse(BaseModel):
    item_id: UUID
    quantity: int
