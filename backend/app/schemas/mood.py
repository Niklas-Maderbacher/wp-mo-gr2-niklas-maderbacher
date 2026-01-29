from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date as dt_date

from app.models.mood_enum import MoodEnum

class MoodBase(BaseModel):
    mood: MoodEnum = Field(...)

class MoodCreate(MoodBase):
    pass

class MoodUpdate(BaseModel):
    mood: Optional[MoodEnum] = None

class MoodInDB(MoodBase):
    daily_report_id: int

    class Config:
        from_attributes = True
