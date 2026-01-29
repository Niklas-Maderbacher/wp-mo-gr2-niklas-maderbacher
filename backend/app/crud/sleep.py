from sqlalchemy.orm import Session
from app.models.sleep import Sleep
from app.schemas.sleep import SleepBase, SleepCreate, SleepUpdate, SleepInDB
from app.models.daily_report import DailyReport
from datetime import datetime, timezone
from app.exceptions.sleep import SleepNotFoundException, SleepCreationException

def create_sleep(*, db: Session, sleep: SleepCreate, daily_report: DailyReport):
    if db.query(Sleep).filter(Sleep.daily_report_id == daily_report.id).first() is not None:
        raise SleepCreationException()

    db_sleep = Sleep(
        duration=sleep.duration,
        daily_report_id=daily_report.id,
    )
    db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return db_sleep
    
def get_sleep(*, db: Session, daily_report: DailyReport):
    sleep = db.query(Sleep).filter(Sleep.daily_report_id == daily_report.id).first()

    if not sleep:
        raise SleepNotFoundException(daily_report.id)
    
    return sleep
    
def get_sleeps(db: Session):
    sleeps = db.query(Sleep).all()

    if len(sleeps == 0):
        raise SleepNotFoundException(-1)
    
    return sleeps
    
def update_sleep(*, db: Session, daily_report: DailyReport, sleep_update: SleepUpdate):
    db_sleep = db.query(Sleep).filter(Sleep.daily_report_id == daily_report.id).first()
    if not db_sleep:
        raise SleepNotFoundException(daily_report.id)
    if sleep_update.duration is not None:
        db_sleep.duration = sleep_update.duration
    db.commit()
    db.refresh(db_sleep)
    return db_sleep

    
def delete_sleep(*, db: Session, daily_report: DailyReport):
    db_sleep = db.query(Sleep).filter(Sleep.daily_report_id == daily_report.id).first()
    if not db_sleep:
        raise SleepNotFoundException(daily_report.id)
    db.delete(db_sleep)
    db.commit()
    return db_sleep
