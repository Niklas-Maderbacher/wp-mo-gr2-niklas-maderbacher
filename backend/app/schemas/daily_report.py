from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date as dt_date

from app.schemas.mood import MoodBase
from app.schemas.sleep import SleepBase
from app.schemas.activity import ActivityBase

from app.models.mood_enum import MoodEnum

class DailyReportBase(BaseModel):
    id: int
    date: dt_date

class DailyReportInDB(BaseModel):
    id: int
    user_id: int
    date: dt_date

    class Config:
        from_attributes = True

