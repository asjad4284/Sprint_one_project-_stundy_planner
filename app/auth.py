from jose import jwt ,JWTError
from datatime import datatime ,timedelta
from fastapi import Header , HTTPException
SECRET_KEY ="supersecretkey"
ALGORITHM ="HS256"

def create_token(data : dict):
    to_encode=data.copy()
    expire =datatime.utcnow()+timedelta(hours=2)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

