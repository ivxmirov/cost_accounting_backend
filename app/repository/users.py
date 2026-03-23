from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserResponse


def get_user(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).scalar()


def create_user(db: Session, login: str) -> UserResponse:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user
