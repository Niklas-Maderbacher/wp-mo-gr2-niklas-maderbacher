from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import activity as crud
from app.schemas import activity as schemas
from app.models.daily_report import DailyReport
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser, get_current_daily_report
from app.exceptions.activity import ActivityNotFoundException

router = APIRouter()

router = APIRouter(prefix="/activities", tags=["activities"])

@router.post("/", response_model=schemas.ActivityBase)
def create_activity(
    db: SessionDep,
    activity: schemas.ActivityCreate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    return crud.create_activity(db=db, activity=activity, daily_report=daily_report)

@router.get("/",
            dependencies=[Depends(get_current_active_superuser)],
            response_model=List[schemas.ActivityInDB]
)
def get_activities(db: SessionDep):
    try:
        return crud.get_activities(db=db)
    except ActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.get("/me", response_model=List[schemas.ActivityBase])
def get_activity(
    db: SessionDep,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        return crud.get_own_activities(db=db, daily_report=daily_report)
    except ActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.put("/me/", response_model=schemas.ActivityBase)
def update_activity(
    db: SessionDep,
    activity_update: schemas.ActivityUpdate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        return crud.update_activity(db=db, daily_report=daily_report, activity_update=activity_update)
    except ActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.delete("/me", response_model=schemas.ActivityBase)
def delete_activity(
    db: SessionDep,
    activity_id: int,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        return crud.delete_activity(db=db, daily_report=daily_report, activity_id=activity_id)
    except ActivityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )