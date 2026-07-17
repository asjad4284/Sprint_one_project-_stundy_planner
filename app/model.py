from sqlalchemy import Column,Integer, Sting , Foreginkey
from app.database import base 

class user(base):
    __tablename__ ="users"
    
    id = Column (Integer , primarykey=True)
    email = Column(Sting(100), unique = True)
    password = Column(Sting(159))

    

