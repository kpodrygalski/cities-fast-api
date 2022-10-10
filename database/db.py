from sqlmodel import Session, create_engine
from models import city, hero, team


URL = "postgresql+psycopg2://minima:P$55word@192.168.8.192/cities_db"
engine = create_engine(URL, echo=True)


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    city.City.metadata.create_all(engine)
    hero.Hero.metadata.create_all(engine)
    team.Team.metadata.create_all(engine)


create_tables()
