from fastapi import APIRouter, Depends, HTTPException, status

from database.db import get_session
from models.city import City, CityRead, CityCreate, CityPatchName, CityPatchCapital

from sqlmodel import Session, select

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=list[City])
async def get_all_cities(session: Session = Depends(get_session)):
    cities = session.exec(select(City)).all()
    return cities


@router.get("/{city_id}", response_model=CityRead)
async def get_city_by_id(city_id: int, session: Session = Depends(get_session)):
    city = session.get(City, city_id)
    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID = {city_id} was not found",
        )
    return city


@router.post('/', response_model=CityRead, status_code=status.HTTP_201_CREATED)
async def create_new_city(city: CityCreate, session: Session = Depends(get_session)):
    db_city = City.from_orm(city)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Something went wrong!')
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


@router.patch('/{city_id}/name', response_model=CityRead)
async def patch_city_name_by_id(city_id: int, city: CityPatchName, session: Session = Depends(get_session)):
    db_city = session.get(City, city_id)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City with ID = {city_id} was not found!")
    city_data = city.dict(exclude_unset=True)
    for key, value in city_data.items():
        setattr(db_city, key, value)
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


@router.patch('/{city_id}/capital', response_model=CityRead)
async def patch_city_name_by_id(city_id: int, city: CityPatchCapital, session: Session = Depends(get_session)):
    db_city = session.get(City, city_id)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City with ID = {city_id} was not found!")
    city_data = city.dict(exclude_unset=True)
    for key, value in city_data.items():
        setattr(db_city, key, value)
    session.add(db_city)
    session.commit()
    session.refresh(db_city)
    return db_city


@router.delete('/{city_id}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_city_by_id(city_id: int, session: Session = Depends(get_session)):
    city = session.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"City with ID = {city_id} was not found!")
    session.delete(city)
    session.commit()
    return None
