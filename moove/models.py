from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(150), nullable=False)
    photo_path = Column(String, default="www.my-photo.com/example")
    password_hash = Column(String(100), nullable=False)
    # Add password_salt when we authenticate
    # password_salt = Column(String)  Add in


