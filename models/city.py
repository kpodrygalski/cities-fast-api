from typing import Optional

from sqlmodel import SQLModel, Field


class CityBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    capital_city: str = Field(max_length=50, unique=True, index=True)


class City(CityBase, table=True):
    __tablename__: str = "cities"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class CityRead(CityBase):
    id: int


class CityCreate(CityBase):
    pass


class CityPatchName(SQLModel):
    name: str


class CityPatchCapital(SQLModel):
    capital_city: str
