from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=15)
    email: EmailStr = Field(..., min_length=7, max_length=50)



class UserCreate(UserBase):
    password: str = Field(..., min_length=1, max_length=50)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=15)
    email: Optional[EmailStr] = Field(None, min_length=7, max_length=50)
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    is_superuser: bool = False

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    pw_hash: str
