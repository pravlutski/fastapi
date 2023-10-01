from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from managers.user import UserManager
from models.user import User


class UserListSchema(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: list[UserListSchema]


class UserDetailResponse(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserCreateRequest(BaseModel):
    """ create user """
    first_name: str = Field(default='John', min_length=3, max_length=20)
    last_name: str = Field(default='Doe', min_length=3, max_length=20)
    email: EmailStr


class UserCreateResponse(BaseModel):
    """ response after create user """
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserUpdateRequest(BaseModel):
    """ update user """
    first_name: str = Field(..., min_length=3, max_length=20)
    last_name: str = Field(..., min_length=3, max_length=20)


class UserUpdateResponse(BaseModel):
    """ response after update user """
    first_name: Optional[str]
    last_name: Optional[str]
