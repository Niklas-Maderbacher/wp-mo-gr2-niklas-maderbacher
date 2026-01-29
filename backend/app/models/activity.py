from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.database.session import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("activity_categories.id", ondelete="CASCADE"), nullable=False)
    duration = Column(Integer, nullable=False)