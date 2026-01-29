from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import Enum as SQL_ENUM

from app.database.session import Base
from app.models.mood_enum import MoodEnum

class Mood(Base):
    __tablename__ = "moods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id", ondelete="CASCADE"), nullable=False)
    mood = Column(SQL_ENUM(MoodEnum), nullable=False)
