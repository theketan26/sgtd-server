from fastapi import APIRouter, Depends
from modules.event.event import Event
from modules.auth.auth import get_current_user


end = Event()

event_router = APIRouter()

@event_router.get('/get-event/{date}')
async def get_event(date, current_user: dict = Depends(get_current_user)):
    report = end.get_events(date)
    return report


@event_router.get('/get-events/{date}/{to}')
async def get_events(date, to):
    report = end.get_events(date, int(to))
    return report


@event_router.post('/add-event/{date}')
async def add_event(date, event_data: dict, current_user: dict = Depends(get_current_user)):
    report = end.add_event(date,
                           summary = event_data['summary'],
                           description = event_data['description'],
                           location = event_data['location'])
    return report


@event_router.delete('/delete-event/{date}/{summary}')
async def delete_event(date, summary, current_user: dict = Depends(get_current_user)):
    report = end.delete_event(date, summary)
    return report


@event_router.post('/update-event')
async def update_event(data: dict, current_user: dict = Depends(get_current_user)):
    report = end.update_event(data['date'], data['old_summary'], data['summary'], data['description'], data['location'])
    return report


