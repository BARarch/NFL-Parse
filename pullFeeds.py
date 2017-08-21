import pandas as pd
from datetime import datetime
import itemQuery as iq
import articleParse as ap
from timeit import default_timer as timer
import subprocess
import modelGS as mgs
#import httplib2
#from apiclient import discovery

#%run modelInit.py

def getFeeds():
    """Google Sheets API Code.
    Pulls urls for all NFL Team RSS Feeds
    https://docs.google.com/spreadsheets/d/1DUBb9OG1A1Xs6v2PK9Oislz4384DSu2MzEbH8dK0ad4/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    #specify sheetID and range
    spreadsheetId = '1DUBb9OG1A1Xs6v2PK9Oislz4384DSu2MzEbH8dK0ad4'
    rangeName = 'Sheet1!A2:E'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Done')

    return values

def writeLinkData(dataColumns):
    """Google Sheets API Code.

    Writes all team news link data from RSS feed to the NFL Team Articles speadsheet.
    https://docs.google.com/spreadsheets/d/1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ/edit#gid=0
    """
    credentials = get_credentials()
    http = credentials.authorize(mgs.httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = mgs.discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheet_id = '1XiOZWw3S__3l20Fo0LzpMmnro9NYDulJtMko09KsZJQ'
    value_input_option = 'RAW'
    rangeName = 'Sheet1!A2'
    values = dataColumns
    body = {
          'values': values
    }
    
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=rangeName,
                                                    valueInputOption=value_input_option, body=body).execute()

    return result

def sheetColumns(record):
    return [record['pubDate'], record['team'], record['title'], record['type'], record['link'], record['discription'], record['creator']]

def getTime(date):
    return datetime.strptime(date[:25], '%a, %d %b %Y %H:%M:%S')

def feedFrame(feedRow):
    return [{'pubDate':record[0], 
             'team':feedRow[1], 
             'title':record[1], 
             'type':feedRow[2], 
             'link':record[2], 
             'discription':record[3], 
             'creator':record[4]
            } for record in iq.recordsFromFeed(feedRow[3])]


get_credentials = mgs.modelInit()

# Step 1 Load Feed Information
feeds = getFeeds()

# Step 2 Pull all feeds from RSS Lins Using feedFram()
data = []
for feedRow in feeds:
    if feedRow[3] == 'null':
        continue
    data.extend(feedFrame(feedRow))
    print('team: '+ feedRow[1] + ' ' + feedRow[0] )

# Step 3 Sort the Data by pubData and DataFrame the result    
dataSorts = sorted(data, key=lambda k: getTime(k['pubDate']), reverse=True)
df = pd.DataFrame(dataSorts)

# Final Step Write the Result to the NFL Feeds Speadsheet.
writeLinkData([sheetColumns(record) for record in dataSorts])

