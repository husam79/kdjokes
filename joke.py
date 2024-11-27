from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Joke(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    source: str
    created_on: str = Field(default=datetime.now())

