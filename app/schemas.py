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

class