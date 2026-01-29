from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
from app.database.session import Base

class Sleep(Base):
    __tablename__ = "sleeps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    daily_report_id = Column(Integer, ForeignKey("daily_reports.id", ondelete="CASCADE"), nullable=False)
    duration = Column(Integer, nullable=False)