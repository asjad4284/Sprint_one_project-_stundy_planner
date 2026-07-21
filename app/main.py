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
# /me is used to checking currently logged in user using token
@app.get("/me")  
def me(payload : dict = Depends(verify_token)):
    return{
        "email":payload.get("sub")
    }    

@app.post("/subjects",response_model=schemas.SubjectResponse)    
def create_subject(subject :schemas.SubjectCreate,db :Session =Depends(get_db)):
    return crud.create_subject(db,subject)  
                 
@app.get("/subject/{user_id}", response_model=list[schemas.SubjectResponse])  
def list_subjects(user_id:int ,db:Session =Depends(get_db)):
    return crud.get_subject(db ,user_id)
# adding deleting feature 
@app.delete("/subjects/{subject_id}")
def  delete_subject(subject_id:int,db:Session=Depends(get_db)):
    result= crud.delete_subject(db,subject_id)
    if  not result:
        raise HTTPException(status_code=404,detail="Subject not found")
    return {"msg": "Deleted"}

@app.post("/schedule", response_model = schemas.ScheduleCreate)
def create_schedule(schedule: schemas.ScheduleCreate,db:Session =Depends(get_db)):
    return crud.create_schedule(db,schedule)

@app.get("/schedule/{user_id}")
def get_schedule(user_id :int , db: Session =Depends(get_db)):
    return crud.get_schedule_for_user(db, user_id)

@app.get("/schedule/today/{user_id}")
def today_schedule(user_id:int , db:Session=Depends(get_schedule)):
    return crud.get_today_schedule(db ,user_id)





