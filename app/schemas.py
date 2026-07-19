from pydantic import BaseModel , Field, EmailStr
""" EmailStr checking  speical  format of email
    Field is using to validate the passwoed"""

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config: #there we  its read the attributes  then convert into jason response on bases of schema
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


