from os import path
import datetime as dt
from datetime import datetime, timedelta


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class App:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.creds = None

        if path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json')

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file('creds.json', self.SCOPES)
                self.creds = flow.run_local_server(port = 0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        try:
            self.service = build('calendar', 'v3', credentials = self.creds)

        except HttpError as err:
            print(err)

    def get_events(self, from_date, to_data = 1):
        try:
            start_datetime = datetime.strptime(from_date, '%Y-%m-%d')
            end_datetime = start_datetime + timedelta(days = to_data)

            start_time = str(start_datetime.strftime('%Y-%m-%d')) + 'T00:00:00-00:00'
            end_time = str(end_datetime.strftime('%Y-%m-%d')) + 'T00:00:00-00:00'

            events_result = self.service.events().list(
                calendarId = 'primary',
                timeMin = start_time,
                timeMax = end_time,
                singleEvents = True,
                orderBy = 'startTime'
            ).execute()

            events = events_result.get('items', [])
            return events

        except HttpError as err:
            print(f"An error occurred: {err}")
            return None


    # def add_event(self, date, summary, description = None, location = None):
    #     try:
    #         # Convert the input date to datetime object
    #         event_date = datetime.strptime(date, '%Y-%m-%d')
    #
    #         # Format datetime object to RFC3339 format required by Google Calendar API
    #         event_time = event_date.isoformat() + 'Z'
    #
    #         # Create event body
    #         event = {
    #             'summary': summary,
    #             'description': description,
    #             'location': location,
    #             'start': {
    #                 'dateTime': event_time,
    #                 'timeZone': 'UTC',
    #             },
    #             'end': {
    #                 'dateTime': event_time,
    #                 'timeZone': 'UTC',
    #             },
    #         }
    #
    #         # Call the Google Calendar API to add the event
    #         created_event = self.service.events().insert(
    #             calendarId='primary',
    #             body=event
    #         ).execute()
    #
    #         print(f"Event '{summary}' added on {date}.")
    #         return created_event
    #
    #     except HttpError as err:
    #         print(f"Google Calendar API Error: {err}")
    #         return None
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    #         return None
