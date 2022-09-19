from sqlmodel import Session, create_engine

from core.config import settings

engine = create_engine(settings.DATABASE_URI, echo=True)

session = Session(engine)
