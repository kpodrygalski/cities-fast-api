from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from database.db import get_session
from models.city import City, CityRead, CityCreate, CityPatchName, CityPatchCapital

from sqlmodel import Session, select

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get(
    "/", response_model=Union[list[City], CityRead, str], status_code=status.HTTP_200_OK
)
async def get_all_cities(
    query: str
    | None = Query(
        default=None, description="Search by city name.", min_length=3, max_length=25
    ),
    session: Session = Depends(get_session),
) -> Union[list[City], CityRead, str]:
    if query:
        stmt = select(City).where(City.name == query)
        founded_cities = session.exec(stmt).first()
        if founded_cities is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with query param = {query} not found!",
            )
        return founded_cities
    cities = session.exec(select(City)).all()
    return cities


@router.get("/{city_id}", response_model=CityRead, status_code=status.HTTP_200_OK)
async def get_city_by_id(
    city_id: int = Path(title="City ID", description="Get city by ID param."),
    session: Session = Depends(get_session),
) -> CityRead:
    city = session.get(City, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID = {city_id} was not found",
        )
    return city


@router.post("/", response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_new_city(
    city: CityCreate, session: Session = Depends(get_session)
) -> CityRead:
    db_city = City.from_orm(city)
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong!"
        )
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


@router.patch(
    "/{city_id}/name", response_model=CityRead, status_code=status.HTTP_200_OK
)
async def patch_city_name_by_id(
    city: CityPatchName,
    city_id: int = Path(title="City ID", description="Patch city name by ID"),
    session: Session = Depends(get_session),
) -> CityRead:
    city_db = session.get(City, city_id)
    if not city_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID = {city_id} was not found!",
        )
    city_data = city.dict(exclude_unset=True)
    for key, value in city_data.items():
        setattr(city_db, key, value)
    session.add(city_db)
    session.commit()
    session.refresh(city_db)
    return city_db


@router.patch(
    "/{city_id}/capital", response_model=CityRead, status_code=status.HTTP_200_OK
)
async def patch_city_name_by_id(
    city: CityPatchCapital,
    city_id: int = Path(
        title="City ID", description="Patch city capital name by city ID."
    ),
    session: Session = Depends(get_session),
) -> CityRead:
    city_db = session.get(City, city_id)
    if not city_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID = {city_id} was not found!",
        )
    city_data = city.dict(exclude_unset=True)
    for key, value in city_data.items():
        setattr(city_db, key, value)
    session.add(city_db)
    session.commit()
    session.refresh(city_db)
    return city_db


@router.delete(
    "/{city_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_city_by_id(
    city_id: int = Path(title="City ID", description="Delete city by ID."),
    session: Session = Depends(get_session),
) -> None:
    city = session.get(City, city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID = {city_id} was not found!",
        )
    session.delete(city)
    session.commit()
    return None
