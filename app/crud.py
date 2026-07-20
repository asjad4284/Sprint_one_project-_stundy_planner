from datetime import datetime
from sqlalchemy.orm import Session
from app import model
from app.utils import hash_password, verify_password
from app.auth import create_token

Day_Map={0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"fri",5:"Sat",6:"Sun"}
# creating  new  user  in  database 
def create_user(db:Session ,user):
    existing= db.query(model.user).filter(model.user.email == user.email).first()

    if existing:
        return None
    obj = model.user(email=user.email , password =hash_password(user.password))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def login_user(db:Session, email ,password):
    user= db.query(model.user).filter(model.user.email ==email).first()
    if not  user or not verify_password(password, user.password):
        return None
    
    token = create_token({"sub":user.email})
    return{
        "access_token" :token , "user_id":user.id
    }

