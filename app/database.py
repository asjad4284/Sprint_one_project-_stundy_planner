from sqlalchemy import create_engine
from  sqlalchemy.orm import  sessionmaker,declarative_base
# At that point  you will go to MySql manully and create datbase with name of study_planner
database_url= "mysql+pymysql://saqlain:shah001@localhost/study_planner"
engine =create_engine(database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
