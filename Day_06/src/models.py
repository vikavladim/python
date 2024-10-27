from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, Table, ForeignKey, \
    UniqueConstraint, Enum
from sqlalchemy.types import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import settings
from ship_pb2 import Alignment
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import enum

Base = declarative_base()

ship_officers = Table('ship_officers', Base.metadata,
                      Column('ship_id', Integer(), ForeignKey("spaceships.id")),
                      Column('officer_id', Integer(), ForeignKey("officers.id"))
                      )

class Alignment(enum.Enum):
    Ally = 'Ally'
    Enemy = 'Enemy'

class Spaceship(Base):
    __tablename__ = 'spaceships'

    id = Column(Integer, primary_key=True)
    alignment = Column(Enum(Alignment))
    name = Column(String)
    ship_class = Column(String)
    length = Column(Float)
    crew_size = Column(Integer)
    is_armed = Column(Boolean)
    speed = Column(Float, nullable=True, default=0.0)
    officers = relationship("Officer", secondary=ship_officers, backref="spaceships")


class Officer(Base):
    __tablename__ = 'officers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    rank = Column(String)

    unique_officer = UniqueConstraint(first_name, last_name, rank)


engine = create_engine(settings.DATABASE_URL_psycopg)
Session = sessionmaker(bind=engine)
session = Session()
