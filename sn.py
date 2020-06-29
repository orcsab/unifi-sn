# sn.py
# ServiceNow functionality
# Help from https://pypi.org/project/servicenow/

import requests
import json

class ServiceNow:
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}
    session = 0
    instance = ''

    def __init__ (self, instance, usr, pwd):
        self.instance = instance
        self.session = requests.Session()
        self.session.auth = (usr, pwd)

    def getRecords (self, table):
        url = f"{self.instance}/api/now/table/{table}"
        r = self.session.get (url, headers=self.headers)
        return r.json()['result']

    def addRecord (self, table, record):
        url = f"{self.instance}/api/now/table/{table}"
        r = self.session.post (url, headers=self.headers, data=json.dumps(record))

        if r.status_code != 201:
            raise Exception(f'addRecord failed with code {r.status_code}: {record}')

        return r.json()
