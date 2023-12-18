from fastapi import APIRouter, Depends
from modules.db.db import Db
from modules.auth.auth import get_current_user
from pydantic import BaseModel


db_router = APIRouter()

db = Db()


async def get_user(user: int):
    report = db.get_user(user)
    return report


class UserDetails(BaseModel):
    number: int
    name: str
    email: str
    position: int

class UserCreds(BaseModel):
    number: int
    password: str

@db_router.post('/add-user')
async def add_user(data: UserCreds, current_user: dict = Depends(get_current_user)):
    report = db.add_user({
        'number': data.number,
        'password': data.password
    })
    return report


@db_router.delete('/delete-user/{number}')
async def delete_user(number: int, current_user: dict = Depends(get_current_user)):
    report = db.delete_user(number)
    return report


@db_router.post('/update-user')
async def update_user(data: UserDetails, current_user: dict = Depends(get_current_user)):
    report = db.update_user(data)
    return report


@db_router.post('/update-user-password')
async def update_user(data: UserCreds, current_user: dict = Depends(get_current_user)):
    report = db.update_password(data)
    return report



