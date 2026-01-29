from sqlalchemy.orm import Session
from app.models.user import User
from app.models.daily_report import DailyReport
from app.schemas.daily_report import DailyReportBase, DailyReportInDB
from datetime import datetime, timezone
from app.exceptions.daily_report import DailyReportDateNotFoundException, DailyReportIdNotFoundException

def create_daily_report(*, db: Session, user: User):
    db_report = DailyReport(
        user_id=user.id,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return db_report

def get_current_daily_report(*, db: Session, user: User):
    today = datetime.now(timezone.utc).date()

    report = db.query(DailyReport).filter(
        DailyReport.user_id == user.id,
        DailyReport.date == today
    ).first()

    if not report:
        raise DailyReportDateNotFoundException(today)
    
    return report

def get_daily_report_by_date(*, db: Session, user: User, date: datetime):
    daily_report = db.query(DailyReport).filter(
        DailyReport.user_id == user.id,
        DailyReport.date == date.date()
    ).first()

    if not daily_report:
        raise DailyReportDateNotFoundException(date)

def get_daily_reports(*, db: Session):
    return db.query(DailyReport).all()

def delete_daily_report_by_id(*, db: Session, report_id: int):
    report = db.query(DailyReport).filter(DailyReport.id == report_id).first()
    if not report:
        raise DailyReportIdNotFoundException(report_id)

    db.delete(report)
    db.commit()

    return report