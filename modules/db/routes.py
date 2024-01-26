from fastapi import APIRouter, Depends
from modules.db.db import Db
from modules.auth.auth import get_current_user
from pydantic import BaseModel


db_router = APIRouter()

db = Db()


async def get_user(user: int):
    report = db.get_user(user)
    return report


async def get_user_detail(user: int):
    report = db.get_user(user, detail = True)
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
async def add_user(data: UserCreds):
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
async def update_user(data: UserDetails):
    report = db.update_user(data)
    return report


@db_router.post('/update-user-password')
async def update_user(data: UserCreds, current_user: dict = Depends(get_current_user)):
    report = db.update_password(data)
    return report


@db_router.get('/get-event-date/{date}')
async def get_event_date(date: str, current_user: dict = Depends(get_current_user)):
    report = db.get_event_on_date(date)
    return report


@db_router.get('/get-event-id/{date}/{id}')
async def get_event_date(date: str, id: str, current_user: dict = Depends(get_current_user)):
    report = db.get_event_on_id(date, id)
    return report


@db_router.get('/get-event-month/{date}')
async def get_event_date(date: str, current_user: dict = Depends(get_current_user)):
    report = db.get_event_on_month(date)
    return report


@db_router.delete('/delete-event/{date}/{event_id}')
async def get_event(date: str, event_id: str, current_user: dict = Depends(get_current_user)):
    report = db.delete_event({
        'date': date,
        'event_id': event_id
    })
    return report


class EventHost(BaseModel):
    name: str
    number: int
    alt_number: int
    address: str
class EventBooker(BaseModel):
    name: str
    number: int
class EventPayment(BaseModel):
    total: int
    deposit: int
    mode: str
    date: str
class EventDesc(BaseModel):
    title: str
    host: EventHost
    booker: EventBooker
    referer: EventBooker
class EventData(BaseModel):
    date: str
    days: int
    desc: EventDesc
    payment: EventPayment


@db_router.post('/add-event')
async def get_event(data: EventData, current_user: dict = Depends(get_current_user)):
    report = db.add_event(data)
    return report


class EventDataUpdate(BaseModel):
    event_id: str
    data: EventData


@db_router.post('/update-event')
async def update_event(data: EventDataUpdate, current_user: dict = Depends(get_current_user)):
    report = db.update_event(data)
    return report

