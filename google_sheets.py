import pickle
import os.path
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1ib1GLhTgbUhRhT7pM9x0hIhPXdFmxwTN0njJGxo7lVk'
RANGE = 'Donations!A2:I1000'


def get_creds():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token_file:
            creds = pickle.load(token_file)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('google_creds.json', SCOPES)
            creds = flow.run_local_server(port=0, success_message='Thanks for signing in. You can close this tab now.')

        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)

    return creds


service = build('sheets', 'v4', credentials=get_creds())
sheet = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()


def get_donations():
    donations = []

    for row in sheet['values']:
        if len(row) > 8 and row[8].lower() == 'true':
            continue

        donation_id = f'{row[1]}-{row[5]}'
        if len(donations) == 0 or donation_id != donations[-1]['donation_id']:
            donations.append(dict(
                donation_date=datetime.strptime(row[5], '%Y-%m-%d'),
                donor_name=row[1], donor_details=row[2],
                donated_items=[], donation_id=donation_id,
            ))

        donations[-1]['donated_items'].append(dict(
            name=row[0], value=float(row[3].replace('$', ''))
        ))

    return donations
