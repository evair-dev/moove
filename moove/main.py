from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=user, user_id=user_id)


@app.patch("/users/{user_id}/photo", response_model=schemas.User)
def upload_photo(user_id: int, user: schemas.UserPhoto, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.upload_user_photo(db=db, user=user, user_id=user_id)


@app.delete("/users/{user_id}/photo", response_model=schemas.User)
def upload_photo(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user_photo(db=db, user_id=user_id)


@app.post("/users/{user_id}/lists", response_model=schemas.UserList)
def create_list_for_user(
    user_id: int, item: schemas.ListCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, user_list=item, user_id=user_id)


@app.get("/users/{user_id}/lists", response_model=List[schemas.UserList])
def get_user_lists(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_lists_from_user(db=db, user_id=user_id)


@app.get("/users/{user_id}/lists/{list_id}", response_model=schemas.UserList)
def get_user_lists(user_id: int, list_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_a_list_from_user(db=db, user_id=user_id, list_id=list_id)


@app.patch("/lists/{list_id}", response_model=schemas.UserList)
def update_list(list_id: int, lists: schemas.ListUpdate, db: Session = Depends(get_db)):
    db_list = crud.get_list(db, list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return crud.update_list(db, lists, list_id)


@app.patch("/lists/{list_id}", response_model=schemas.UserList)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    db_list = crud.get_list(db, list_id)
    if db_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return crud.delete_list(db, list_id)
