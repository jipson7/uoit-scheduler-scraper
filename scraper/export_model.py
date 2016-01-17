
from model import Base

from sqlalchemy import create_engine

engine = create_engine('sqlite:///schedule.db')

Base.metadata.create_all(engine)
