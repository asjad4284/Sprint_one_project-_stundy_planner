from pydantic import BaseModel , Field, EmailStr
from typing import Dict
""" EmailStr checking  speical  format of email
    Field is using to validate the passwoed"""

class UserCreate(BaseModel):
    email: EmailStr
    password:str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config: #there its read the attributes  then convert into jason response on bases of schema
        from_attributes = True

class SubjectCreate(BaseModel):
    name :str
    difficulty :str
    hours: int =Field(gt=0)
    user_id : int

class SubjectResponse(BaseModel):
    id :int
    name :str
    difficulty : str
    hours : int
    user_id: int
    class Config:
        from_attributes = True
class ScheduleCreate(BaseModel):
    day : int
    duration :int
    subject_id: int

class ScheduleResponse(BaseModel):
    id :int
    day:int
    duration:int
    subject_id :int
    class Config:
        from_attribute = True

class ProgressCreste(BaseModel):
    status: str
    schedule_id = int

class ProgressResponse(BaseModel):
    id : int
    status : str
    schedule_id: int
    class Config:
        from_attribute = True
        
            





