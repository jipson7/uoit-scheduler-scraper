import os
from sqlalchemy import Column, Integer, String, ForeignKey, Time, Date, create_engine
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))              # Max found = 57
    department = Column(String(4))
    code = Column(String(5))
    section = Column(String(3))
    capacity_total = Column(Integer)
    capacity_taken = Column(Integer)
    capacity_remaining = Column(Integer)
    semester = Column(String(6))

class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    class_type = Column(String(16)) # Max Found = 5
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    day = Column(String(1))
    location = Column(String(128))
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    section_type = Column(String(32)) # Max found = 17
    instructors = Column(String(256)) # Max found = 202
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship(Course, backref=backref("days", cascade="all, delete-orphan"))

try:
    engine = create_engine(os.environ['SCRAPE_DATABASE'])
except Exception as e:
    print(e)
    raise

Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
