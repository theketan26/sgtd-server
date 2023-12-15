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

    def get_events(self, date):
        try:
            # Convert the input date to datetime object
            start_datetime = datetime.strptime(date, '%Y-%m-%d')
            end_datetime = start_datetime + timedelta(days = 1)  # Events for the entire day

            # Format datetime objects to RFC3339 format required by Google Calendar API
            start_time = start_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')
            end_time = end_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')

            # Call the Google Calendar API to get events for the specified date
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