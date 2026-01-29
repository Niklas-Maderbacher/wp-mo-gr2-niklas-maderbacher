from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date as dt_date

class SleepBase(BaseModel):
    duration: int = Field(...)

class SleepCreate(SleepBase):
    pass

class SleepUpdate(BaseModel):
    duration: Optional[int] = None

class SleepInDB(BaseModel):
    daily_report_id: int
    duration: int

    class Config:
        from_attributes = True

class SleepAdminView(SleepBase):
    username: str = Field(...)
    date: dt_date