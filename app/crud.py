from sqlalchemy.orm import Session

from models import UserTable
from schema import User


def create_user(db: Session, user: User):
    db_user = UserTable(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(UserTable).filter(UserTable.email == email).first()
