from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
from app.database.session import Base
from datetime import date


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, default=date.today(), nullable=False)
