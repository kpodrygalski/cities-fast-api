from sqlmodel import Session, create_engine
from models.city import City

URL = "postgresql+psycopg2://minima:P$55word@192.168.8.192/cities_db"
engine = create_engine(URL, echo=True)


# Dependency
def get_session():
    with Session(engine) as session:
        yield session


def create_tables():
    City.metadata.create_all(engine)


create_tables()
