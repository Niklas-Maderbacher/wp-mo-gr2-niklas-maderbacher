from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import daily_report as crud
from app.schemas import daily_report as schemas
from app.api.deps import SessionDep, CurrentUser,get_current_active_superuser, get_current_user
from app.exceptions.daily_report import DailyReportDateNotFoundException, DailyReportIdNotFoundException

router = APIRouter()

router = APIRouter(prefix="/daily_reports", tags=["daily_reports"])

@router.post("/create", response_model=schemas.DailyReportBase)
def create_daily_report(db: SessionDep, current_user: CurrentUser):
    return crud.create_daily_report(db=db, user=current_user)

@router.get(
    "/current",
    response_model=schemas.DailyReportBase,
)
def get_current_daily_report(db: SessionDep, current_user: CurrentUser):
    try:
        return crud.get_current_daily_report(db=db, user=current_user)
    except DailyReportDateNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.get(
    "/{date}",
    response_model=schemas.DailyReportBase,
)
def get_daily_report_by_date(db: SessionDep, date: str, current_user: CurrentUser):
    try:
        return crud.get_daily_report_by_date(db=db, user=current_user, date=date)
    except DailyReportDateNotFoundException as e:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.get(
    "/all",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[schemas.DailyReportBase],
)
def get_daily_reports(db: SessionDep):
    return crud.get_daily_reports(db=db)

@router.delete(
    "/{report_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=bool,
)
def delete_daily_report_by_id(db: SessionDep, report_id: int):
    try:
        return crud.delete_daily_report_by_id(db=db, report_id=report_id)
    except DailyReportIdNotFoundException as e:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )