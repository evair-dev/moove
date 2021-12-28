from sqlalchemy import Boolean, Date, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(150), nullable=False)
    photo_path = Column(String, default="Not found")
    password_hash = Column(String(100), nullable=False)
    # Add password_salt when we authenticate
    # password_salt = Column(String)  Add in
    lists = relationship("UserList", back_populates="owner")


class UserList(Base):
    __tablename__ = "user_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(250))
    public = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="lists")
    movies = relationship('Movie', secondary='movie_user_list')


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    tagline = Column(String)
    overview = Column(String)
    release_date = Column(Date)
    poster_url = Column(String)
    backdrop_url = Column(String)
    imdb_id = Column(String)

    user_lists = relationship('UserList', secondary='movie_user_list')


class MovieUserList(Base):
    __tablename__ = 'movie_user_list'

    user_lists_id = Column(
      Integer,
      ForeignKey('user_lists.id'),
      primary_key=True)
    movies_id = Column(
        Integer,
        ForeignKey('movies.id'),
        primary_key=True)
