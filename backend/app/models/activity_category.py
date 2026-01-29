from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.session import Base

class ActivityCategory(Base):
    __tablename__ = "activity_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)