import datetime as dt

from fastapi import FastAPI

from modules.setup.setup import App


app = FastAPI()
end = App()


@app.get('/')
async def root():
    return {
        'message': 'Working'
    }


@app.get('/get-event/{date}')
async def get_event(date):
    report = end.get_events(date)
    return {
        'message': report
    }


@app.get('/get-events/{date}/{to}')
async def get_event(date, to):
    report = end.get_events(date, int(to))
    return {
        'message': report
    }
