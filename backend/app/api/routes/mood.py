from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import mood as crud
from app.schemas import mood as schemas
from app.models.daily_report import DailyReport
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser, get_current_daily_report
from app.exceptions.mood import MoodNotFoundException, MoodCreationException

router = APIRouter()

router = APIRouter(prefix="/moods", tags=["moods"])

@router.post("/", response_model=schemas.MoodBase)
def create_mood(
    db: SessionDep,
    mood: schemas.MoodCreate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        db_mood = crud.create_mood(db=db, mood=mood, daily_report=daily_report)

        return schemas.MoodBase(
            mood=db_mood.mood,
        )
    except MoodCreationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )

@router.get("/",
            dependencies=[Depends(get_current_active_superuser)],
            response_model=List[schemas.MoodInDB]
)
def get_moods(db: SessionDep):
    try:
        db_moods = crud.get_moods(db=db)
    
        response = []

        for db_mood in db_moods:
            response.append(schemas.MoodInDB(
                mood=db_mood.mood,
                daily_report_id=db_mood.daily_report_id,
            ))

        return response
    except MoodNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.get("/me", response_model=schemas.MoodBase)
def get_mood(
    db: SessionDep,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        db_mood = crud.get_mood(db=db, daily_report=daily_report)

        if db_mood is None:
            raise MoodNotFoundException(daily_report.id)

        return schemas.MoodBase(
            mood=db_mood.mood,
        )
    except MoodNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.put("/me", response_model=schemas.MoodBase)
def update_mood(
    db: SessionDep,
    mood_update: schemas.MoodUpdate,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        db_mood = crud.update_mood(db=db, daily_report=daily_report, mood_update=mood_update)

        if db_mood is None:
            raise MoodNotFoundException(daily_report.id)

        return schemas.MoodBase(
            mood=db_mood.mood,
        )
    except MoodNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

@router.delete("/me", response_model=schemas.MoodBase)
def delete_mood(
    db: SessionDep,
    daily_report: DailyReport = Depends(get_current_daily_report),
):
    try:
        db_mood = crud.delete_mood(db=db, daily_report=daily_report)

        return schemas.MoodBase(
            mood=db_mood.mood,
        )
    except MoodNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )