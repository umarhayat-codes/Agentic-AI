from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from os import getenv
import jwt

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    try: 
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,  SECRET_KEY , algorithm=ALGORITHM)
    except Exception as e:
        print('An exception occurred')
        print(e)
        return None
    
def verify_token(token: str=Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        if decoded_token:
            return decoded_token
        else:
            raise HTTPException(status_code=401, detail="Token not parsable")
    except Exception as e:
        print('An exception occurred')
        print(str(e))
        raise HTTPException(status_code=401, detail="Token decorded") 
    
