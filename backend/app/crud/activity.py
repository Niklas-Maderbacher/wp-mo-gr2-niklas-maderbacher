from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityBase, ActivityCreate, ActivityUpdate, ActivityInDB
from app.models.daily_report import DailyReport
from datetime import datetime, timezone
from app.exceptions.activity import ActivityNotFoundException

def create_activity(*, db: Session, activity: ActivityCreate, daily_report: DailyReport):
    db_activity = Activity(
        name=activity.name,
        duration=activity.duration,
        category_id=activity.category_id,
        daily_report_id=daily_report.id,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_own_activities(*, db: Session, daily_report: DailyReport):
    activities = db.query(Activity).filter(Activity.daily_report_id == daily_report.id).all()

    if len(activities) == 0:
        raise ActivityNotFoundException(-1)
    
    return activities

def get_activities(db: Session):
    return db.query(Activity).all()


def update_activity(*, db: Session, daily_report: DailyReport, activity_id: int, activity_update: ActivityUpdate):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not db_activity:
        raise ActivityNotFoundException(activity_update.id)
    if activity_update.name is not None:
        db_activity.name = activity_update.name
    if activity_update.duration is not None:
        db_activity.duration = activity_update.duration
    if activity_update.category_id is not None:
        db_activity.category_id = activity_update.category_id

    db.commit()
    db.refresh(db_activity)
    return db_activity

def delete_activity(*, db: Session, daily_report: DailyReport, activity_id: int):
    db_activity = db.query(Activity).filter(Activity.daily_report_id == daily_report.id, Activity.id == activity_id).first()
    if not db_activity:
        raise ActivityNotFoundException(activity_id)
    db.delete(db_activity)
    db.commit()
    return db_activity