from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ActivityCategoryBase(BaseModel):
    id: int
    name: str = Field(...)

class ActivityCategoryCreate(BaseModel):
    name: str = Field(...)

class ActivityCategoryUpdate(BaseModel):
    id: int
    name: Optional[str] = None

class ActivityCategoryInDB(ActivityCategoryBase):
    class Config:
        from_attributes = True