from typing import List, Optional

from sqlmodel import Relationship, SQLModel, Field

# from models.hero import Hero, HeroRead


class TeamBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    headquaters: str


class Team(TeamBase, table=True):
    __tablename__: str = "teams"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    heroes: List["Hero"] = Relationship(back_populates="team")


class TeamRead(TeamBase):
    id: int


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass


# class TeamWithHeroRead(TeamRead):
#     heroes: List[HeroRead] = []
