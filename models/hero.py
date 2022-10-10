from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from models.team import Team, TeamRead


class HeroBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    secret_name: str = Field(index=True)
    age: Optional[int] = Field(default=1, index=True)


class Hero(HeroBase, table=True):
    __tablename__: str = "heroes"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    # Teams -> beacuse our table name of team model is Teams
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    team: Optional[Team] = Relationship(back_populates="heroes")


class HeroRead(HeroBase):
    id: int


class HeroCreate(HeroBase):
    team_id: Optional[int]


class HeroReadWithTeams(HeroRead):
    team: Optional[TeamRead] = None
