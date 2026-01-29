from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date as dt_date

class ActivityBase(BaseModel):
    id: int
    name: str = Field(...)
    duration: int = Field(...)
    category_id: int = Field(...)

    class Config:
        from_attributes = True

class ActivityCreate(BaseModel):
    name: str = Field(...)
    duration: int = Field(...)
    category_id: int = Field(...)

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    category_id: Optional[int] = None

class ActivityInDB(ActivityBase):
    daily_report_id: int

    class Config:
        from_attributes = True

class ActivityAdminView(BaseModel):
    username: str = Field(...)
    date: dt_date