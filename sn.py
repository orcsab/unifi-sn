# sn.py
# ServiceNow functionality
# Help from https://pypi.org/project/servicenow/

import requests
import json
import datetime

from pprint import pprint

class ServiceNow:
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}
    session = 0
    instance = ''

    def __init__ (self, instance, usr, pwd):
        self.instance = instance
        self.session = requests.Session()
        self.session.auth = (usr, pwd)

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
    def addRecord (self, table, record):
        url = f"{self.instance}/api/now/table/{table}"
        r = self.session.post (url, headers=self.headers, data=json.dumps(record))

        if r.status_code != 201:
            raise Exception(f'addRecord failed with code {r.status_code}: {record}')
        else:
            pprint(r.json())

        return r.json()

    # addMetric
    # Add a metric to the time series. Table, sysId and metric name must be specified.
    def addMetric (self, table, sysId, metric, value):
        url = f'{self.instance}/api/now/v1/clotho/put'

        j = {
            'seriesRef': {
                'subject': sysId,
                'table': table,
                'metric': metric
            },
            'values': [
                {
                    'timestamp': datetime.datetime.utcnow().replace(microsecond=0).isoformat(),
                    'value': value
                }
            ]
        }

        r = self.session.post (url, headers=self.headers, data=json.dumps(j))
        if r.status_code != 200:
            raise Exception (f'addMetric failed with code {r.status_code}: {r}')
