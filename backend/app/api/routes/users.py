from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.crud import user as crud
from app.schemas import user as schemas
from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.exceptions.user import UserNotFoundException, UserExistsException


router = APIRouter()

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=schemas.UserBase,
)
def get_self(db: SessionDep, current_user: CurrentUser):
    user = crud.get_current_user(db=db, current_user=current_user)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return schemas.UserBase(
        username=user.username,
        email=user.email,
    )

@router.get(
    "/superusers",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[schemas.User],
)
def get_superusers(db: SessionDep):
    users = crud.get_superusers(db=db)

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No superusers found"
        )

    response = []

    for user in users:
        response.append(
            schemas.User(
                id=user.id,
                username=user.username,
                email=user.email,
                is_superuser=user.is_superuser,
            )
        )
    
    return response

@router.get(
    "/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=schemas.UserBase,
)
def get_user_by_email(db: SessionDep, email: str):
    try:
        user = crud.get_user_by_email(db=db, email=email)

        if user is None:
            raise UserNotFoundException(message="User not found")

        return schemas.UserBase(
            username=user.username,
            email=user.email,
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.get(
    "/{username}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=schemas.UserBase,
)
def get_user_by_username(db: SessionDep, username: str):
    try:
        user = crud.get_user_by_username(db=db, username=username)

        if user is None:
            raise UserNotFoundException(message="User not found")

        return schemas.UserBase(
            username=user.username,
            email=user.email,
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )

@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[schemas.User],
)
def get_users(db: SessionDep):
    users = crud.get_users(db=db)

    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found"
        )

    response = []

    for user in users:
        response.append(
            schemas.User(
                id=user.id,
                username=user.username,
                email=user.email,
                is_superuser=user.is_superuser,
            )
        )
    
    return response

@router.post("/", response_model=schemas.UserBase)
def create_user(db: SessionDep, user: schemas.UserCreate):
    try:
        user = crud.create_user(db=db, user=user)

        return schemas.UserBase(
            username=user.username,
            email=user.email,
        )
    except UserExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )

@router.post(
        "/superusers",
        dependencies=[Depends(get_current_active_superuser)],
        response_model=schemas.User
)
def create_superuser(db: SessionDep, user: schemas.UserCreate):
    try:
        user = crud.create_superuser(db=db, user=user)

        return schemas.User(
            id=user.id,
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
        )
    except UserExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )

@router.put("/me", response_model=schemas.UserBase)
def update_user(db: SessionDep, user_update: schemas.UserUpdate, current_user: CurrentUser):
    try:
        user = crud.update_user(db=db, current_user=current_user, user_update=user_update)

        return schemas.UserBase(
            username=user.username,
            email=user.email,
        )
    except UserExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )

@router.delete("/me", response_model=schemas.UserBase)
def delete_user(db: SessionDep, current_user: CurrentUser):
    user = crud.delete_current_user(db=db, current_user=current_user)

    return schemas.UserBase(
        username=user.username,
        email=user.email,
    )

@router.delete(
        "/{user_id}",
        dependencies=[Depends(get_current_active_superuser)],
        response_model=schemas.User)
def delete_user_by_id(*, db: SessionDep, user_id: int):
    try:
        user = crud.delete_user_by_id(db=db, user_id=user_id)

        return schemas.User(
            id=user.id,
            username=user.username,
            email=user.email,
            is_superuser=user.is_superuser,
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
