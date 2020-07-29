# sn.py
# ServiceNow functionality
# Help from https://pypi.org/project/servicenow/

import requests
import json
import datetime
import configparser
import os
import sys

from pprint import pprint

class ServiceNow:
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}
    session = 0
    instance = ''

    def __init__ (self, cfgfile):
        file = os.path.join (sys.path[0], cfgfile)

        if not os.path.isfile(file):
            raise Exception (f'__init__: no such file: {file}')

        config = configparser.ConfigParser()
        config.read(file)

        self.instance = config['instance']['url']
        self.session = requests.Session()
        self.session.auth = (config['credentials']['name'],
                             config['credentials']['pass'])

    # getRecords
    # Get all records from the named table.
    def getRecords (self, table):
        url = f"{self.instance}/api/now/table/{table}"
        r = self.session.get (url, headers=self.headers)
        if r.status_code != 200:
            raise Exception (f'getRecords failed with code {r.status_code}: {r}')

        return r.json()['result']

    # addRecord
    # Add the JSON in 'record' to the table. If there is a field mismatch This
    # will behave unpredictably.
    # table: the table to which the record will be added
    # record: the record to add. must use fields in the aforementioned table or expect a crash
    # returns: the added record
    def addRecord (self, table, record):
        url = f"{self.instance}/api/now/table/{table}"
        r = self.session.post (url, headers=self.headers, data=json.dumps(record))

        if r.status_code != 201:
            raise Exception(f'addRecord failed with code {r.status_code}: {record}')
        else:
            pprint(r.json())

        return r.json()['result']

    # addMetric
    # Add a metric to the time series. Table, sysId and metric name must be specified.
    # table: the table containing the sysId
    # sysId: the record (in the above table) to which the metric should be attached
    # metric: the name of the metric (timeseries)
    # value: the value to store
    # timestamp: the timestamp at which the metric was measured/observed
    def addMetric (self, table, sysId, metric, value, timestamp):
        url = f'{self.instance}/api/now/v1/clotho/put'

        j = {
            'seriesRef': {
                'subject': sysId,
                'table': table,
                'metric': metric
            },
            'values': [
                {
                    'timestamp': timestamp,
                    'value': value
                }
            ]
        }

        r = self.session.post (url, headers=self.headers, data=json.dumps(j))
        if r.status_code != 200:
            raise Exception (f'addMetric failed with code {r.status_code}: {r}')
