from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Sheet:

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, spreadsheet_id: str = ''):

        self.__creds = None
        self._service = self.get_service()
        self._sheet = self._service.spreadsheets()
        self._spreadsheet_id = spreadsheet_id

    def get_service(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.__creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=self.__creds)
            return service
        except Exception as e:
            print(e)
            return None

    def update(self, row: str = '', text: str = ''):
        body = {
            "majorDimension": "ROWS",
            "values": [
                [
                    text
                ]
            ],
            "range": row
        }

        self._sheet.values().update(spreadsheetId=self._spreadsheet_id, range=row,
                                    valueInputOption='USER_ENTERED', body=body).execute()

    def add_row(self, value):
        body = {
            "majorDimension": "ROWS",
            "values": [
                [
                    value
                ]
            ],
            "range": 'A1'
        }

        self._sheet.values().append(spreadsheetId=self._spreadsheet_id, range='A1',
                                    valueInputOption='USER_ENTERED', body=body).execute()

    def get(self, row: str = ''):
        result = self._sheet.values().get(spreadsheetId=self._spreadsheet_id,
                                          range=row).execute()

        return result

    def float_row(self, row):
        # if row is zero don't move
        if row == 1:
            return
        body = {
            "moveDimension": {
                "source": {
                    "dimension": "ROWS",
                    "startIndex": row - 1,
                    "endIndex": row
                },
                "destinationIndex": 0
            }
        }
        reqs = {
            "requests": [body]
        }

        self._sheet.batchUpdate(spreadsheetId=self._spreadsheet_id, body=reqs).execute()

    def find_tag_id(self, id=''):
        result = self._sheet.values().get(spreadsheetId=self._spreadsheet_id,
                                          range="A1:A40").execute()
        c = 0
        for i in result['values']:
            c += 1
            print(i, 'FIND TAG')
            if i[0] == id:
                print(i, c)
                return c
        else:
            return None


if __name__ == '__main__':
    sheet = Sheet('1UXQ1YRHduKlEbhRDUChRh1D-F2ln75VLQ9c7yE_69BU')
    item = sheet.get('A1')

    sheet.find_tag_id("abcdefg")
