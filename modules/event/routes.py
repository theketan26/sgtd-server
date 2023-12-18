from fastapi import APIRouter, Depends
from modules.event.event import Event
from modules.auth.auth import get_current_user
from pydantic import BaseModel
import json


end = Event()

event_router = APIRouter()

@event_router.get('/get-event-description/{date}')
async def get_event_description(date: str, current_user: dict = Depends(get_current_user)):
    report = end.get_events(date)
    return report


@event_router.get('/get-events/{date}/{to}')
async def get_events(date: str, to: int):
    report = end.get_events(date, to)
    return report


class EventDescription(BaseModel):
    host_name: str
    host_number: int
    host_email: str
    host_address: str
    booker_name: str
    booker_number: int
    dates: list
    days: int

class EventModel(BaseModel):
    summary: str
    description: EventDescription
    location: str

@event_router.post('/add-event/{date}')
async def add_event(date: str, event_data: EventModel, current_user: dict = Depends(get_current_user)):
    report = end.add_event(date,
                           summary = event_data.summary,
                           description = json.dumps({
                                'host_name': event_data.description.host_name,
                                'host_number': event_data.description.host_number,
                                'host_email': event_data.description.host_email,
                                'host_address': event_data.description.host_address,
                                'booker_name': event_data.description.booker_name,
                                'booker_number': event_data.description.booker_number,
                                'dates': ','.join(event_data.description.dates)
                           }),
                           day = event_data.description.days,
                           location = event_data.location)
    return report


@event_router.delete('/delete-event/{date}/{summary}')
async def delete_event(date: str, summary: str, current_user: dict = Depends(get_current_user)):
    report = end.delete_event(date, summary)
    return report


class NewEventModel(BaseModel):
    old_summary: str
    summary: str
    description: EventDescription
    location: str

@event_router.post('/update-event/{date}')
async def update_event(date: str, data: NewEventModel, current_user: dict = Depends(get_current_user)):
    report = end.update_event(date,
                              data.old_summary,
                              data.summary,
                              json.dumps({
                                  'host_name': data.description.host_name,
                                  'host_number': data.description.host_number,
                                  'host_email': data.description.host_email,
                                  'host_address': data.description.host_address,
                                  'booker_name': data.description.booker_name,
                                  'booker_number': data.description.booker_number,
                                  'dates': ','.join(data.description.dates)
                              }),
                              data.location)
    return report


