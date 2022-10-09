from sqlmodel import Session, create_engine
from models.city import City
from models.hero import Hero
from models.team import Team
from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")
engine = create_engine(config["PSQL_URL"], echo=True)


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    City.metadata.create_all(engine)
    Team.metadata.create_all(engine)
    Hero.metadata.create_all(engine)


create_tables()
