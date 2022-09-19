from sqlmodel import SQLModel

from db import engine
from models.session import Session  # noqa
from models.user import User  # noqa


def init_db():
    SQLModel.metadata.create_all(engine)


init_db()
