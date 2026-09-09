
from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1024)


class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
