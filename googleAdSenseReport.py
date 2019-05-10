from flask import Response
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials
from pytz import timezone
from oauth2client.file import Storage
import datetime
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']
KEY_FILE_LOCATION = './keys/client_secrets.json'
CREDENTIALS_FILE_LOCATION = './keys/credentials.json'
storage = Storage(CREDENTIALS_FILE_LOCATION)

def initialize_adsense_reporting():
    # flow = flow_from_clientsecrets(KEY_FILE_LOCATION,
                                   # SCOPES,
                                   # redirect_uri='http://localhost:8080/')
    # auth_uri = flow.step1_get_authorize_url()
    # print(auth_uri)
    # code = ""
    # credentials = flow.step2_exchange(code)
    # storage.put(credentials)
    # credentials = storage.get()

    with open(CREDENTIALS_FILE_LOCATION) as credentials_json:
        credentials_dict = json.load(credentials_json)
        credentials = OAuth2Credentials(
            refresh_token = credentials_dict["refresh_token"],
            token_uri = credentials_dict["token_uri"],
            client_id = credentials_dict["client_id"],
            client_secret = credentials_dict["client_secret"],
            access_token = credentials_dict["access_token"],
            token_expiry = credentials_dict["token_expiry"],
            user_agent = credentials_dict["user_agent"],
        )

        adsense = build('adsense', 'v1.4', credentials=credentials)
        print(adsense)
    # return adsense

def get_report(adsense):
    now_pacific = datetime.datetime.now(timezone('US/Pacific'))
    today_pacific = now_pacific.strftime('%Y-%m-%d')

    yesterday_pacific = now_pacific - datetime.timedelta(6)
    yesterday_pacific = yesterday_pacific.strftime('%Y-%m-%d')

    return adsense.reports().generate(
        startDate = yesterday_pacific, 
        endDate = today_pacific,
        # filter=['AD_CLIENT_ID==' + ad_client_id],
        metric=['EARNINGS'],
        dimension=['DATE', 'DOMAIN_NAME'],
        #sort=['+DATE']
    ).execute()

def return_adsense_report():
    adsense = initialize_adsense_reporting()
    report = get_report(adsense)
    earnings = {}
    result = {}
    for row in report.get('rows', []):
        if row[1] == 'ucsb.tokyo':
            earnings.update({ row[0]: row[2] })
    totals = report.get('totals', [])
    result.update({ 
        'earnings': earnings, 
        'total': totals[2] 
    }) 
    resp = Response()
    resp.status_code = 200
    resp.set_data(json.dumps(result))
    pp.pprint(result)
    return resp

initialize_adsense_reporting()
