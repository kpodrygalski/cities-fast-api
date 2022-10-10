from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.hero import Hero


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List[Hero] = Relationship(back_populates="team")
