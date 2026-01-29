from sqlalchemy.orm import Session
from app.models.activity_category import ActivityCategory
from app.schemas.activity_category import ActivityCategoryBase, ActivityCategoryCreate, ActivityCategoryUpdate, ActivityCategoryInDB
from app.models.daily_report import DailyReport
from datetime import datetime, timezone
from app.exceptions.activity_category import ActivityCategoryAlreadyExistsException, ActivityCategoryNotFoundException, NoActivityCategoriesExsitsYetException

def create_activity_category(*, db: Session, activity_category: ActivityCategoryCreate):
    if db.query(ActivityCategory).filter(ActivityCategory.name == activity_category.name).first() is not None:
        raise ActivityCategoryAlreadyExistsException()

    db_activity_category = ActivityCategory(
        name=activity_category.name,
    )
    db.add(db_activity_category)
    db.commit()
    db.refresh(db_activity_category)
    return db_activity_category

def get_activity_category(*, db: Session, activity_category_id: int):
    db_activity_category = db.query(ActivityCategory).filter(ActivityCategory.id == activity_category_id).first()

    if db_activity_category is None:
        raise ActivityCategoryNotFoundException(activity_category_id)

    return db_activity_category

def get_activity_categories(db: Session):
    db_activity_categories = db.query(ActivityCategory).all()

    if len(db_activity_categories) == 0:
        raise NoActivityCategoriesExsitsYetException()
    
    return db_activity_categories


def update_activity_category(*, db: Session, activity_category_id: int, activity_category_update: ActivityCategoryUpdate):
    db_activity_category = db.query(ActivityCategory).filter(ActivityCategory.id == activity_category_id).first()
    if not db_activity_category:
        raise ActivityCategoryNotFoundException(activity_category_id)
    if db.query(ActivityCategory).filter(ActivityCategory.name == activity_category_update.name).first() is not None:
        raise ActivityCategoryAlreadyExistsException()
    if activity_category_update.name is not None:
        db_activity_category.name = activity_category_update.name
    db.commit()
    db.refresh(db_activity_category)
    return db_activity_category

def delete_activity_category(*, db: Session, activity_category_id: int):
    db_activity_category = db.query(ActivityCategory).filter(ActivityCategory.id == activity_category_id).first()
    if not db_activity_category:
        raise ActivityCategoryNotFoundException(activity_category_id)
    db.delete(db_activity_category)
    db.commit()
    return db_activity_category