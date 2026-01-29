from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import sleep as crud
from app.schemas import sleep as schemas
from app.models.daily_report import DailyReport
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser, get_current_daily_report
from app.exceptions.sleep import SleepNotFoundException, SleepCreationException

router = APIRouter()

router = APIRouter(prefix="/sleeps", tags=["sleeps"])

@router.post("/", response_model=schemas.SleepBase)
def create_sleep(
    db: SessionDep,
    sleep: schemas.SleepCreate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        sleep = crud.create_sleep(db=db, sleep=sleep, daily_report=daily_report)

        return schemas.SleepBase(
            duration=sleep.duration,
        )
    except SleepCreationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    
@router.get("/",
            dependencies=[Depends(get_current_active_superuser)],
            response_model=List[schemas.SleepInDB]
)
def get_sleeps(db: SessionDep):
    try:
        sleeps_db = crud.get_sleeps(db=db)

        if sleeps_db is None:
            raise SleepNotFoundException(-1)

        response = []

        for sleep in sleeps_db:
            response.append(schemas.SleepInDB(
                id=sleep.id,
                daily_report_id=sleep.daily_report_id,
                duration=sleep.duration,
            ))
    except SleepNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    
@router.get("/me", response_model=schemas.SleepBase)
def get_sleep(
    db: SessionDep,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        sleep = crud.get_sleep(db=db, daily_report=daily_report)

        if sleep is None:
            raise SleepNotFoundException(-1)
        
        return schemas.SleepBase(
            duration=sleep.duration,
        )
    except SleepNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    
@router.put("/me", response_model=schemas.SleepBase)
def update_sleep(
    db: SessionDep,
    sleep_update: schemas.SleepUpdate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        sleep = crud.update_sleep(db=db, daily_report=daily_report, sleep_update=sleep_update)

        if sleep is None:
            raise SleepNotFoundException(-1)
        
        return schemas.SleepBase(
            duration=sleep.duration,
        )
    except SleepNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

@router.delete("/me", response_model=schemas.SleepBase)
def delete_sleep(
    db: SessionDep,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        sleep = crud.delete_sleep(db=db, daily_report=daily_report)

        if sleep is None:
            raise SleepNotFoundException(-1)

        return schemas.SleepBase(
            hours=sleep.hours,
        )
    except SleepNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)