from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from utils.helpers import uuid4_str

if TYPE_CHECKING:
    from models.session import Session


class UserBase(SQLModel):
    name: str
    focused: bool = True


class User(UserBase, table=True):  # type: ignore
    id: Optional[str] = Field(default_factory=uuid4_str, primary_key=True)
    session_id: str = Field(foreign_key="session.id")
    session: "Session" = Relationship(back_populates="users")
