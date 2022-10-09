from typing import Union
from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from sqlmodel import Session, select
from database.db import get_session

from models.team import Team, TeamCreate, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get(
    "/", response_model=Union[list[Team], TeamRead, str], status_code=status.HTTP_200_OK
)
async def get_all_teams(
    query: str = Query(default=None, description="Search team by name."),
    session: Session = Depends(get_session),
) -> Union[list[Team], TeamRead, str]:
    if query:
        stmt = select(Team).where(Team.name == query)
        team = session.exec(stmt).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with query name = {query} not found!",
            )
        return team
    teams = session.exec(select(Team)).all()
    if not teams:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teams not found!"
        )
    return teams


@router.get("/{team_id}", response_model=TeamRead, status_code=status.HTTP_200_OK)
async def get_team_by_id(
    team_id: int = Path(default=None, title="Team ID", description="Get team by id."),
    session: Session = Depends(get_session),
) -> TeamRead:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID = {team_id} not found!",
        )
    return team


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
async def create_new_team(
    team: TeamCreate, session: Session = Depends(get_session)
) -> TeamRead:
    team_db = Team.from_orm(team)
    if not team_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create new team!"
        )
    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db


@router.put("/{team_id}", response_model=TeamRead, status_code=status.HTTP_200_OK)
async def update_team_by_id(
    *,
    team_id: int = Path(
        default=None, title="Team ID", description="Get team to update by ID."
    ),
    team: TeamUpdate,
    session: Session = Depends(get_session),
) -> TeamRead:
    team_db = session.get(Team, team_id)
    if not team_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID = {team_id} not found!",
        )
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team_db, key, value)
    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db


@router.delete(
    "/{team_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_team_by_id(
    *,
    team_id: int = Path(
        default=None, title="Team ID", description="Delete team by id."
    ),
    session: Session = Depends(get_session),
) -> None:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID = {team_id} not found!",
        )
    session.delete(team)
    session.commit()
    return None


# @router.get(
#     "/{team_id}/heroes", response_model=TeamWithHeroRead, status_code=status.HTTP_200_OK
# )
# async def get_team_by_id_with_heroes(
#     *,
#     team_id: int = Path(
#         default=None, title="Team ID", description="Get team by ID with heroes."
#     ),
#     session: Session = Depends(get_session),
# ) -> TeamWithHeroRead:
#     team = session.get(Team, team_id)
#     if not team:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Team with ID = {team_id} not found!",
#         )
#     return team
