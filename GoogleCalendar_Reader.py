from __future__ import print_function
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

calendar_id = "your calendar id"

class Writer(object):
    def __init__(self):
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
            """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def google_calendar_reader(self):

            events_result = self.service.events().list(
                calendarId= calendar_id,
                q="test",
                timeMin = "2020-02-01T00:00:00+00:00",
                timeMax = "2020-02-29T00:00:00+00:00",
                timeZone = None,
                singleEvents=True,
                orderBy="startTime",
                ).execute()
            events = events_result.get("items", [])

            if not events:
                print("not found")
            for event in events:
                start = event['start'].get('dateTime',event['start'].get('date'))
                description = event.get('description', "not found")
                print(start)
                print("Event :",event['summary'])
                print("Description :",description,"\n")

writer = Writer()
writer.google_calendar_reader()
