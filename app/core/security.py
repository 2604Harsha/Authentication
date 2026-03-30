import uuid
from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime,timedelta
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str, hashed:str) -> str:
    return pwd_context.verify(password, hashed)

def create_access_token(data:dict, minutes:int = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=minutes
    )
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, settings.SECRET_KEY,
    algorithm=settings.ALGORITHM
    )

def create_refresh_token():
    return str(uuid.uuid4())