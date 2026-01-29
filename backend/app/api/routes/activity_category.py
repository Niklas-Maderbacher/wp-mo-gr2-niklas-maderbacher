from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import activity_category as crud
from app.schemas import activity_category as schemas
from app.models.daily_report import DailyReport
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser, get_current_daily_report
from app.exceptions.activity_category import ActivityCategoryAlreadyExistsException, ActivityCategoryNotFoundException, NoActivityCategoriesExsitsYetException

router = APIRouter()

router = APIRouter(prefix="/activity-categories", tags=["activity-categories"])

@router.post("/", response_model=schemas.ActivityCategoryBase)
def create_activity_category(db: SessionDep, activity_category: schemas.ActivityCategoryCreate):
    try:
        return crud.create_activity_category(db=db, activity_category=activity_category)
    except ActivityCategoryAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=e.message
        )

@router.get(
    "/{activity_category_id}",
    response_model=schemas.ActivityCategoryBase
)
def get_activity_category(db: SessionDep, activity_category_id: int):
    try:
        return crud.get_activity_category(db=db, activity_category_id=activity_category_id)
    except ActivityCategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.get(
    "/",
    response_model=List[schemas.ActivityCategoryBase],
)
def get_activity_categories(db: SessionDep):
    try:
        return crud.get_activity_categories(db=db)
    except NoActivityCategoriesExsitsYetException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.put(
    "/{activity_category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=schemas.ActivityCategoryBase
)
def update_activity_category(db: SessionDep, activity_category_id: int, activity_category_update: schemas.ActivityCategoryUpdate):
    try:
        return crud.update_activity_category(
            db=db,
            activity_category_id=activity_category_id,
            activity_category_update=activity_category_update,
        )
    except ActivityCategoryAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=e.message
        )
    except ActivityCategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.delete(
    "/{activity_category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=schemas.ActivityCategoryBase
)
def delete_activity_category(db: SessionDep, activity_category_id: int):
    try:
        return crud.delete_activity_category(db=db, activity_category_id=activity_category_id)
    except ActivityCategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )