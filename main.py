# coding: utf-8

from flask import Flask, Response
import json
from googleAnalyticsReport import return_analytics_report
from googleAnalyticsPageViewReport import return_analytics_pageview_report
from googleAdSenseReport import return_adsense_report

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    resp = Response()
    resp.status_code = 200
    resp.content_type = 'text/html; charset=utf-8'
    resp.set_data(json.dumps({
        'result': u'This is a kannachan bot server'
    }))
    return resp

@app.route('/googleAnalyticsReport', methods=['GET'])
def googleAnalyticsReport():
    return return_analytics_report()

@app.route('/googleAnalyticsPageViewReport', methods=['GET'])
def googleAnalyticsPageViewReport():
    return return_analytics_pageview_report()

@app.route('/googleAdSenseReport', methods=['GET'])
def googleAdSenseReport():
    return return_adsense_report()

if __name__ == '__main__':
    app.run()
