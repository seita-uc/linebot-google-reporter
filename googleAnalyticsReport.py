from flask import Response
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './keys/service_account.json'
VIEW_ID = '187987801'

def initialize_analytics_reporting():
    credentials = None
    if os.environ['PYTHON_ENV'] == 'test':
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            KEY_FILE_LOCATION, SCOPES
        )
    
    else:
        service_account = json.loads(os.environ['SERVICE_ACCOUNT'])
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
             service_account, SCOPES
        )

    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

def get_report(analytics):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [{'expression': 'ga:pageviews'}],
                    'dimensions': [{'name': 'ga:city'}],
                    "orderBys":[{"fieldName": "ga:pageviews", "sortOrder": "DESCENDING"}]
                }]
        }
    ).execute()

def return_analytics_report():
    analytics = initialize_analytics_reporting()
    response = get_report(analytics)
    result = {}
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    for row in report.get('data', {}).get('rows', []):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])
        for header, dimension in zip(dimensionHeaders, dimensions):
            # print(header + ': ' + dimension)
            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    # print(metricHeader.get('name') + ': ' + value)
                    if dimension == '(not set)':
                        dimension = 'Other'
                    result.update({ dimension: value })

    resp = Response()
    resp.status_code = 200
    resp.set_data(json.dumps(result))
    print(json.dumps(json.loads(resp.get_data()), indent=4, sort_keys=True))
    return resp

# return_analytics_report()
