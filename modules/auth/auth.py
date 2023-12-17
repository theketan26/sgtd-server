from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import json
import requests
import config


with open('consts.json', 'r') as file:
    secret = json.load(file)
    SECRET_KEY = secret['secret_key']
    ALGORITHM = secret['algorithm']


router = APIRouter()

def create_jwt_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": 100000})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl = "token"))):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception


@router.post("/token")
async def login_for_access_token(data: dict):
    user = {"sub": data["username"]}
    access_token = create_jwt_token(data = user)
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}
