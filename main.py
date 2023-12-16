import datetime as dt

from fastapi import FastAPI

from modules.setup.setup import App
from modules.db.db import Db


app = FastAPI()
end = App()
db = Db()


@app.get('/')
async def root():
    return {
        'message': 'Working'
    }


@app.get('/get-event/{date}')
async def get_event(date):
    report = end.get_events(date)
    return report


@app.get('/get-events/{date}/{to}')
async def get_events(date, to):
    report = end.get_events(date, int(to))
    return report


@app.post('/add-event/{date}')
async def add_event(date, event_data: dict):
    report = end.add_event(date,
                           summary = event_data['summary'],
                           description = event_data['description'],
                           location = event_data['location'])
    return report


@app.delete('/delete-event/{date}/{summary}')
async def delete_event(date, summary):
    report = end.delete_event(date, summary)
    return report


@app.post('/update-event')
async def update_event(data: dict):
    report = end.update_event(data['date'], data['old_summary'], data['summary'], data['description'], data['location'])
    return report


@app.post('/add-user/details')
async def add_user_details(data: dict):
    report = db.add_user_details(data)
    return report


@app.post('/add-user')
async def add_user(data: dict):
    report = db.add_user(data)
    return report


@app.delete('/delete-user/{number}')
async def delete_user(number):
    report = db.delete_user(number)
    return report


@app.post('/update_user')
async def update_user(data: dict):
    report = db.update_user(data)
    return report
