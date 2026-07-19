import bcrypt
def hash_password(password:str):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

def verfiy_password(plain , hashed):
    return bcrypt.checkpw(plain.encode(),hashed.encode())
