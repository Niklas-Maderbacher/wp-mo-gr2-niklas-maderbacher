from sqlalchemy.orm import Session
from app.models.mood import Mood
from app.schemas.mood import MoodBase, MoodCreate, MoodUpdate, MoodInDB
from app.models.daily_report import DailyReport
from datetime import datetime, timezone
from app.exceptions.mood import MoodNotFoundException, MoodCreationException

def create_mood(*, db: Session, mood: MoodCreate, daily_report: DailyReport):
    if db.query(Mood).filter(Mood.daily_report_id == daily_report.id).first() is not None:
        raise MoodCreationException()

    db_mood = Mood(
        mood=mood.mood,
        daily_report_id=daily_report.id,
    )
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return db_mood

def get_mood(*, db: Session, daily_report: DailyReport):
    mood = db.query(Mood).filter(Mood.daily_report_id == daily_report.id).first()

    if not mood:
        raise MoodNotFoundException(daily_report.id)
    
    return mood

def get_moods(db: Session):
    moods = db.query(Mood).all()

    if len(moods) == 0:
        raise MoodNotFoundException(-1)
    
    return moods

def update_mood(*, db: Session, daily_report: DailyReport, mood_update: MoodUpdate):
    db_mood = db.query(Mood).filter(Mood.daily_report_id == daily_report.id).first()
    if not db_mood:
        raise MoodNotFoundException(daily_report.id)
    if mood_update.mood is not None:
        db_mood.mood = mood_update.mood
    db.commit()
    db.refresh(db_mood)
    return db_mood


def delete_mood(*, db: Session, daily_report: DailyReport):
    db_mood = db.query(Mood).filter(Mood.daily_report_id == daily_report.id).first()
    if not db_mood:
        raise MoodNotFoundException(daily_report.id)
    db.delete(db_mood)
    db.commit()
    return db_mood
