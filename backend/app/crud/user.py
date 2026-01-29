from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.exceptions.user import UserNotFoundException, UserExistsException
from datetime import datetime, timezone


def create_user(*, db: Session, user: UserCreate):
    try:
        db_user = User(
            username=user.username,
            email=user.email,
            pw_hash=get_password_hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        raise UserExistsException()


def create_superuser(*, db: Session, user: UserCreate):
    try:
        db_user = User(
            username=user.username,
            email=user.email,
            pw_hash=get_password_hash(user.password),
            is_superuser=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        raise UserExistsException()


def get_user(*, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise UserNotFoundException(user_id)

def get_current_user(*, db: Session, current_user: User):
    user = db.query(User).filter(User.id == current_user.id).first()

    if len(user) == 0:
        raise UserNotFoundException(current_user.id)
    
    return user


def get_users(db: Session):
    users = db.query(User).all()

    if len(users) == 0:
        raise UserNotFoundException(-1)
    
    return users

def get_superusers(*, db: Session):
    super_users = db.query(User).filter(User.is_superuser == True).all()

    if len(super_users) == 0:
        raise UserNotFoundException(-1)
    
    return super_users


def authenticate_user(*, db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    if not verify_password(password, str(db_user.pw_hash)):
        return None
    return db_user


def get_user_by_email(*, db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise UserNotFoundException(email)
    
    return user

def get_user_by_username(*, db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise UserNotFoundException(username)
    
    return user

def update_user(*, db: Session, current_user: User, user_update: UserUpdate):
    try:
        if user_update.username is not None:
            current_user.username = user_update.username
        if user_update.email is not None:
            current_user.email = user_update.email
        if user_update.password is not None:
            current_user.pw_hash = get_password_hash(user_update.password)

        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user
    except:
        raise UserExistsException()

def delete_current_user(*, db: Session, current_user: User):
    db.delete(current_user)
    db.commit()
    return current_user

def delete_user_by_id(*, db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundException(user_id)

    db.delete(user)
    db.commit()
    return user
