from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from utils.helpers import uuid4_str

if TYPE_CHECKING:
    from models.user import User


class SessionBase(SQLModel):
    pass


class Session(SessionBase, table=True):  # type: ignore
    id: Optional[str] = Field(default_factory=uuid4_str, primary_key=True)
    users: List["User"] = Relationship(back_populates="session")
