from pydantic import BaseModel


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

    class Config:
        orm_mode = True
