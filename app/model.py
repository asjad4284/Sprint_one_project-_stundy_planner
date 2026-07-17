from sqlalchemy import Column,Integer, Sting , Foreignkey
from app.database import base 

class user(base):
    __tablename__ ="users"
    
    id = Column (Integer , primary_key=True)
    email = Column(Sting(100), unique = True)
    password = Column(Sting(159))

class subject(base):
    __tablename__ ="subjects"
    id = Column(Integer, primary_key=True)
    name =Column(Sting(200))
    difficulty = Column(Sting(150))
    hours=Column(Integer)
    user_id = Column(Integer , ForeignKey("users.id"))


