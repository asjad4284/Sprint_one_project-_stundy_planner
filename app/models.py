from sqlalchemy import Column,Integer, String , ForeignKey
from app.database import Base 

class user(Base):
    __tablename__ ="users"
    
    id = Column (Integer , primary_key=True)
    email = Column(String(100), unique = True)
    password = Column(String(159))

class subject(Base):
    __tablename__ ="subjects"
    id = Column(Integer, primary_key=True)
    name =Column(String(200))
    difficulty = Column(String(150))
    hours=Column(Integer)
    user_id = Column(Integer ,ForeignKey("users.id"))

class schedule(Base):
    __tablename__ ="schedule"
    id = Column(Integer, primary_key=True)
    day = Column(String(200))
    duration = Column(Integer)
    subject_id = Column(Integer , ForeignKey("subjects.id"))

class progress(Base):
    __tablename__ ="progress"
    id =Column(Integer ,primary_key=True)
    status = Column(String(200))
    schedule_id= Column(Integer, ForeignKey("schedule.id"))