from sqlalchemy import create_engine
from  sqlalchemy.orm import  sessionmaker,declarative_base
import os
# At that point  you will go to MySql manully and create datbase with name of study_planner
database_url= os.getenv("DATABASE_URL", "sqlite:///./study_planner.db")
engine =create_engine(database_url,connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base=declarative_base()
def get_db(): # using dependence and also for database automatically closing after using 
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
