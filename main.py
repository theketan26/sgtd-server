import datetime as dt
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from modules.setup.setup import App
from modules.db.db import Db


app = FastAPI()
end = App()
db = Db()

with open('consts.json', 'r') as file:
    secret = json.load(file)
    SECRET_KEY = secret['secret_key']
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 100000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await get_user(int(form_data.username))
    if not result:
        return {
            'status': False,
            'message': 'Incorrect username'
        }

    result['_id'] = str(result['_id'])
    if result['password'] != form_data.password:
        return {
            'status': False,
            'message': 'Incorrect password'
        }

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub": form_data.username},
                                       expires_delta = access_token_expires)
    return {
        'status': True,
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
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


@app.get('/')
async def root():
    return {
        'message': 'Working'
    }


@app.get('/get-event/{date}')
async def get_event(date, current_user: dict = Depends(get_current_user)):
    report = end.get_events(date)
    return report


@app.get('/get-events/{date}/{to}')
async def get_events(date, to):
    report = end.get_events(date, int(to))
    return report


@app.post('/add-event/{date}')
async def add_event(date, event_data: dict, current_user: dict = Depends(get_current_user)):
    report = end.add_event(date,
                           summary = event_data['summary'],
                           description = event_data['description'],
                           location = event_data['location'])
    return report


@app.delete('/delete-event/{date}/{summary}')
async def delete_event(date, summary, current_user: dict = Depends(get_current_user)):
    report = end.delete_event(date, summary)
    return report


@app.post('/update-event')
async def update_event(data: dict, current_user: dict = Depends(get_current_user)):
    report = end.update_event(data['date'], data['old_summary'], data['summary'], data['description'], data['location'])
    return report


async def get_user(user: int):
    report = db.get_user(user)
    return report


@app.post('/add-user/details')
async def add_user_details(data: dict, current_user: dict = Depends(get_current_user)):
    report = db.add_user_details(data)
    return report


class UserCreds(BaseModel):
    user: int
    passwords: str

@app.post('/add-user')
async def add_user(data: UserCreds, current_user: dict = Depends(get_current_user)):
    report = db.add_user({
        'number': data.user,
        'password': data.password
    })
    return report


@app.delete('/delete-user/{number}')
async def delete_user(number, current_user: dict = Depends(get_current_user)):
    report = db.delete_user(number)
    return report


@app.post('/update-user')
async def update_user(data: dict, current_user: dict = Depends(get_current_user)):
    report = db.update_user(data)
    return report



