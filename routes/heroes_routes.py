from typing import Union
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlmodel import Session, select


from database.db import get_session

from models.hero import Hero, HeroCreate, HeroRead, HeroReadWithTeams
from models.team import Team


router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.get(
    "/", response_model=Union[list[Hero], HeroRead, str], status_code=status.HTTP_200_OK
)
async def get_all_heroes(
    query: str
    | None = Query(
        default=None,
        description="Search for heroes by hero name.",
        min_length=2,
        max_length=25,
    ),
    session: Session = Depends(get_session),
) -> Union[list[Hero], HeroRead, str]:
    if query:
        stmt = select(Hero).where(Hero.name == query)
        foundned_heroes = session.exec(stmt).first()
        if not foundned_heroes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Hero with name = {query} not found!",
            )
        return foundned_heroes
    heroes = session.exec(select(Hero)).all()
    return heroes


@router.get("/{hero_id}", response_model=HeroRead, status_code=status.HTTP_200_OK)
async def get_hero_by_id(
    hero_id: int = Path(
        default=None, title="Hero ID", description="Get hero by hero ID."
    ),
    session: Session = Depends(get_session),
) -> HeroRead:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID = {hero_id} not found!",
        )
    return hero


@router.post("/", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
async def create_new_herose(
    hero: HeroCreate, session: Session = Depends(get_session)
) -> HeroRead:
    db_hero = Hero.from_orm(hero)
    if not db_hero:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create new hero!"
        )
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.delete(
    "/{hero_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_hero_by_id(
    hero_id: int = Path(
        default=None, title="Hero ID", description="Delete hero by hero ID"
    ),
    session: Session = Depends(get_session),
) -> None:
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID = {hero_id} not found!",
        )
    session.delete(db_hero)
    session.commit()
    return None


@router.get(
    "/{hero_id}/teams",
    response_model=Union[HeroRead, HeroReadWithTeams],
    status_code=status.HTTP_200_OK,
)
async def get_hero_by_id_with_team(
    *,
    hero_id: int = Path(
        default=None, title="Hero ID", description="Get hero by hero ID with team."
    ),
    show_team: bool = Query(
        default=False, description="Switch showing team relationship True/False."
    ),
    session: Session = Depends(get_session),
) -> Union[HeroRead, HeroReadWithTeams]:
    if show_team:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hero with ID = {hero_id} not found!",
            )
        return hero

    hero_with_team = session.get(Hero, hero_id)
    if not hero_with_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with ID = {hero_id} not found!",
        )
    return hero_with_team


@router.get("/test/", response_model=list[Hero], status_code=status.HTTP_200_OK)
async def get_hero_with_team_test(
    session: Session = Depends(get_session),
):
    stmt = select(Hero, Team).join(Team)
    results = session.exec(stmt).all()
    return results
