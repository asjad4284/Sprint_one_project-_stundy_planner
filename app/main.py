from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm  import Session
from typing import list 
from app.database import engine , get_db
from app import model ,schemas,crud
from app.auth import verify_token

model.Base.metadate.create_all(bind=engine)

app =FastAPI(title="Study Planner")

@app.get("/")
def home():
    return{"Massage":"Study Planner Running"}

@app.post("/user",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db :Session=Depends(get_db)):
    result= crud.create_user(db,user)
    if result is None:
        raise HTTPException(status_code=409 , detail="Email  already Register")
    return result

@app.get("/login")
def login(email:str, password:str,db:Session = Depends(get_db)):
    result = crud.login_user(db,email,password)
    if not result:
        raise HTTPException(status_code=401 , detail="Invalide  credentials")
    return result

                
                 



