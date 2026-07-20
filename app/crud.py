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

def create_subject(db:Session, subject):
    obj = model.subject(**subject.dict()) # subject.dict() is using for unpack the  dictionary 
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_subject(db :Session, user_id :int):
    return db.query(model.subject).filter(model.subject.user_id==user_id).all()

def del_suject(db:Session , subject_id :int):
    obj = db.query(model.subject).filter(model.subject.id==subject_id).first()
    if  not obj:
        return None

    db.delete(obj)
    db.commit()
    return True


def cerate_schedule(db :Session ,schedule):
    obj = model.schedule(**schedule.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    progess =  model.progress(status ="pending" ,schedule_id=obj.id)
    db.add(progess)
    db.commit()
    db.refresh(obj)
    return obj
    
def get_schedule_for_user(db:Session,user_id :int):
    rows =(db.query(model.schedule, model.subject.name).join(model.subject, model.schedule.subject.id==model.subject.id)
          .filter(model.subject.user_id==user_id).all())
    
    return[{
        "id": s.id , "day":s.dat,"duration":s.duration,"subject":s.subject_id,"subject_name":name
    }
    for s ,name in rows]
 


