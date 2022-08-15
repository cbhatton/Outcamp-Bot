from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects', 'https://www.googleapis.com/auth/spreadsheets']

import inspect


class credentials:
    
    def __init__(self):
        """Calls the Apps Script API.
            """
        self.__creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.__creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())

    @property
    def apps_script(self):
        return build('script', 'v1', credentials=self.__creds)

    @property
    def sheets(self):
        return build('sheets', 'v4', credentials=self.__creds)

    @property
    def creds(self):
        return self.__creds.to_json()


if __name__ == '__main__':
    body = {"function": "setActiveSelection"}

    response = credentials().apps_script.scripts().run(scriptId="AKfycbxXQUFK_IxK2ET9QC0xEXRFoRwTK8VVuLNsgnA91Y6vYlX5T7BOBIAFQfY5RM5_zypX",
                                                       body=body).execute()

    print(response)
    # print(dir(credentials().apps_script.projects()))