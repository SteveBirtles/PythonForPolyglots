import httplib2
import os

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
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')   
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)    

    spreadsheet_id = None

    if os.path.isfile("sheetid.txt"):

        with open("sheetid.txt") as file:

            spreadsheet_id = file.read()

    if spreadsheet_id == None:

        spreadsheet_body = {
            'properties': {
                'title': 'API Testing Spreadsheet'
            }
        }

        request = service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()
        
        spreadsheet_id = response['spreadsheetId'];

        with open("sheetid.txt", "w") as file:
            file.write(spreadsheet_id)

    #------------------    


    batch_clear_values_request_body = {        
        'ranges': ['A1:J10']
    }

    service.spreadsheets().values().batchClear(spreadsheetId=spreadsheet_id, body=batch_clear_values_request_body).execute()

    value = lambda x, r, g, b: {         
        'userEnteredValue': {
            'stringValue': str(x)
        },
        'userEnteredFormat': {
            'backgroundColor': {
                'red': r, 
                'green': g, 
                'blue': b, 
                'alpha': 1 
            } 
        }
    }

    data = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(str(i) + ',' + str(j))
        data.append(row)

    rows = [{'values': [value(cell, int(cell.split(',')[0])/10, int(cell.split(',')[1])/10, 0) for cell in row]} for row in data]
    
    body = {
        'requests': [
            {            
                'updateCells': {    
                    'rows': rows,
                    'start': {            
                      "sheetId": 0,
                      "rowIndex": 0,
                      "columnIndex": 0,            
                    },
                    'fields': '*'
                }
            }
        ]
    }

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()




if __name__ == '__main__':

    main()


