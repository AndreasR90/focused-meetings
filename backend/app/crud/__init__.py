from typing import List

from sqlmodel import select

from db import session as db_session
from models.session import Session
from models.user import User


def get_or_create_session(session_id: str) -> Session:
    statement = select(Session).where(Session.id == session_id)
    session = db_session.exec(statement=statement).first()
    if session is None:
        session = create_session(session_id=session_id)
    return session


def create_session(session_id: str) -> Session:
    session = Session(id=session_id)
    db_session.add(session)
    db_session.commit()
    return session


def create_user(user: User) -> User:
    db_session.add(user)
    db_session.commit()
    return user


def get_users(session_id: str) -> List[User]:
    statement = select(User).where(User.session_id == session_id)
    users = db_session.exec(statement=statement).all()
    return users


def toggle_focus(id: str) -> User:
    user = db_session.get(User, id)
    user.focused = not user.focused
    db_session.add(user)
    db_session.commit()
    return user


def delete_user(id: str):
    user = db_session.get(User, id)
    session_id = user.session_id
    db_session.delete(user)
    session = db_session.get(Session, session_id)
    if len(session.users) == 1:
        db_session.delete(session)
    db_session.commit()
