from pydantic import BaseModel
from typing import List, Optional


# For List
class ListBase(BaseModel):
    name: str
    description: Optional[str] = None


class ListCreate(ListBase):
    pass


class ListUpdate(ListBase):
    pass


class UserList(ListBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# For User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    full_name: str
    password: str


class UserUpdate(UserBase):
    full_name: str


class UserPhoto(BaseModel):
    photo_path: str


class User(UserBase):
    id: int
    full_name: str
    photo_path: str
    lists: List[UserList] = []

    class Config:
        orm_mode = True
