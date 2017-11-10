import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = ['https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/spreadsheets']

CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    
    credential_path = 'sheets.googleapis.com-python-quickstart.json'
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():

    current_millisecs = lambda: int(round(time.time() * 1000))
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)    

    spreadsheet_body = {
                            'properties': {
                                'title': 'Test Sheet ' + str(current_millisecs())
                            }
                        }

    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    
    spreadsheet_id = response['spreadsheetId'];

    #------------------    

    value = lambda x: { 
                'userEnteredValue': {
                    'stringValue': str(x)
                },
                'userEnteredFormat': {
                    'backgroundColor': {
                        'red': 0.7, 
                        'green': 0.4, 
                        'blue': 0.2, 
                        'alpha': 1.0
                    } 
                }
            }

    data = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(str(i) + ',' + str(j))
        data.append(row)

    rows = [{'values': [value(cell) for cell in row]} for row in data]
    
    body = {
        'requests': [
            {
                'appendCells': {
                    'sheetId': 0,
                    'rows': rows,
                    'fields': '*',
                }
            }
        ],
    }

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()


if __name__ == '__main__':

    main()