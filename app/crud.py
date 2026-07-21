from datetime import datetime
from sqlalchemy.orm import Session
from app import model
from app.utils import hash_password, verify_password
from app.auth import create_token

Day_Map={0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
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

def del_subject(db:Session , subject_id :int):
    obj = db.query(model.subject).filter(model.subject.id==subject_id).first()
    if  not obj:
        return None

    db.delete(obj)
    db.commit()
    return True


def create_schedule(db :Session ,schedule):
    obj = model.schedule(**schedule.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    progress =  model.progress(status ="pending" ,schedule_id=obj.id)
    db.add(progress)
    db.commit()
    db.refresh(obj)
    return obj
    
def get_schedule_for_user(db:Session,user_id :int):
    rows =(db.query(model.schedule, model.subject.name).join(model.subject, model.schedule.subject_id==model.subject.id)
          .filter(model.subject.user_id==user_id).all())
    
    return[{
        "id": s.id , "day":s.day,"duration":s.duration,"subject":s.subject_id,"subject_name":name
    }

    for s ,name in rows ]

def get_today_schedule(db:Session,user_id :int):
    today_name =Day_Map[datetime.now().weekday()]
    rows=(db.query(model.schedule, model.subject.name,model.progress.status)
          .join(model.subject,model.schedule.subject_id==model.subject.id)
          .outerjoin(model.progress , model.progress.schedule_id==model.schedule.id).filter(model.subject.user_id==user_id ,model.schedule.day == today_name)
          .all())
    
    return [
        {"schedule_id":s.id, "subject":name,"duration": s.duration,"status":status or "pending"}
        for s, name, status in rows
    ]
# update progress 
def update_progress(db :Session,schedule_id :int ,status :str):
    progress = db.query(model.progress).filter(model.progress.schedule_id== schedule_id).first()
    if not progress:
        return None
    progress.status =status
    db.commit()
    db.refresh(progress)
    return progress

def weekly_reports(db:Session ,user_id:int):
    rows=(
        db.query(model.progress ,model.schedule.day).join(model.schedule , model.progress.schedule_id==model.schedule.id)
        .join(model.subject , model.schedule.subject_id== model.subject.id)
        .filter(model.subject.user_id==user_id).all()
    )
    total = len(rows)
    completed = 0
    by_day = {}
    for p, day in rows:
        if p.status == "completed":
            completed += 1

            if day not in by_day:
                by_day[day] = 0

            by_day[day] += 1   

    return{
        "total":total,
        "completed": completed,
        "pending":total-completed,
        "percent":round((completed/total)*100,1) if total else 0.0,
        "by_day":by_day
    }     






























    

    
 


