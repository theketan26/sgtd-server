from fastapi import APIRouter, Depends
from modules.db.db import Db
from modules.auth.auth import get_current_user
from pydantic import BaseModel


db_router = APIRouter()

db = Db()


async def get_user(user: int):
    report = db.get_user(user)
    return report


@db_router.post('/add-user/details')
async def add_user_details(data: dict, current_user: dict = Depends(get_current_user)):
    report = db.add_user_details(data)
    return report


class UserCreds(BaseModel):
    user: int
    passwords: str

@db_router.post('/add-user')
async def add_user(data: UserCreds, current_user: dict = Depends(get_current_user)):
    report = db.add_user({
        'number': data.user,
        'password': data.password
    })
    return report


@db_router.delete('/delete-user/{number}')
async def delete_user(number, current_user: dict = Depends(get_current_user)):
    report = db.delete_user(number)
    return report


@db_router.post('/update-user')
async def update_user(data: dict, current_user: dict = Depends(get_current_user)):
    report = db.update_user(data)
    return report



