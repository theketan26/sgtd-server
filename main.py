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
