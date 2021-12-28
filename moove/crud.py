from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_pass = user.password + "hashed"
    db_user = models.User(email=user.email, full_name=user.full_name, password_hash=hashed_pass)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = get_user(db, user_id)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    return commit_change_in_db_user(db, db_user)


def upload_user_photo(db: Session, user: schemas.UserPhoto, user_id: int):
    db_user = get_user(db, user_id)
    user_data = user.dict(exclude_unset=True)
    setattr(db_user, "photo_path", user_data["photo_path"])

    return commit_change_in_db_user(db, db_user)


def delete_user_photo(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    setattr(db_user, "photo_path", "Not found")

    return commit_change_in_db_user(db, db_user)


def commit_change_in_db_user(db: Session, db_user: schemas.User):
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_item(db: Session, user_list: schemas.ListCreate, user_id: int):
    db_list = models.UserList(**user_list.dict(), owner_id=user_id)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


def get_list_from_user(db: Session, user_id: int):
    return get_user(db, user_id).lists


def get_a_list_from_user(db: Session, user_id: int, list_id: int):
    return db.query(models.UserList).filter(models.UserList.id == list_id, models.UserList.owner_id == user_id).first()


def get_list(db: Session, list_id: int):
    return db.query(models.UserList).filter(models.UserList.id == list_id).first()


def update_list(db: Session, lists: schemas.ListUpdate, list_id: int):
    db_list = get_list(db, list_id)
    user_data = lists.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_list, key, value)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list


def delete_list(db: Session, list_id: int):
    db_list = get_list(db, list_id)
    db.delete(db_list)
    db.commit()
    db.refresh(db_list)
    return {"ok": True}

