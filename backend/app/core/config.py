from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URI: Optional[str] = "sqlite:///test.db"

    class Config:
        case_sensitive = True


load_dotenv()

settings = Settings()
