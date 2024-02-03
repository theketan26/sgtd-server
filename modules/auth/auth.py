import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()


ALGORITHM = "HS256"
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
CRYPTO_KEY = os.getenv('CRYPTO_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 100000


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ENCRYPTION_KEY, algorithm = ALGORITHM)
    return encoded_jwt


async def login_for_access_token(form_data):
    from modules.db.routes import get_user, get_user_detail
    result = await get_user(int(form_data.username))
    if not result:
        return {
            'status': False,
            'message': 'Incorrect username'
        }

    fernet = Fernet(CRYPTO_KEY)

    result['_id'] = str(result['_id'])
    result['password'] = fernet.decrypt(result['password'])
    result['password'] = result['password'].decode('utf-8')
    if result['password'] != form_data.password:
        return {
            'status': False,
            'message': f'Incorrect password'
        }
    
    details_result = await get_user_detail(int(form_data.username))
    details_result.pop('_id')

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": form_data.username},
                                       expires_delta = access_token_expires)

    return {
        'status': True,
        "access_token": access_token,
        "data": details_result,
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ENCRYPTION_KEY, algorithms = [ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception