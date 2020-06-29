# First learned this from From https://github.com/DataKnox/CodeSamples
# Additional API info at https://ubntwiki.com/products/software/unifi-controller/api

import requests
import json
from pprint import pprint
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Unifi:
    body = 0
    port = 0
    baseUrl = ''
    session = 0

    # set REST API headers
    headers = {"Accept": "application/json",
               "Content-Type": "application/json"}


    def __init__ (self, host, port, usr, pwd):
        self.body = {
            "username": usr,
            "password": pwd
        }
        self.host = host
        self.port = port

        # Open a session for capturing cookies
        self.session = requests.Session()
        # login
        loginUrl = 'api/login'
        url = f"https://{self.host}:{self.port}/{loginUrl}"
        response = self.session.post(url, headers=self.headers,
                                data=json.dumps(self.body), verify=False)

        # parse response data into a Python object
        api_data = response.json()
        # print("/" * 50)
        # pprint(api_data)
        # print('Logged in!')
        # print("/" * 50)

    def printDevices (self, siteName):
        getDevicesUrl = f"api/s/{siteName}/stat/device"
        url = f"https://{self.host}:{self.port}/{getDevicesUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        api_data = response.json()
        responseList = api_data['data']
        print('DEVICE LIST AND STATUS')
        for device in responseList:
            print(f"The device {device['name']} has IP {device['ip']}")
            print(f"MAC:            {device['mac']}")
            print(f"DHCP?:          {device['config_network']['type']}")
            if device['state'] == 1:
                print('State:          online')
            else:
                print('State:          offline')
            print(f"Upgradable?     {device['upgradable']}")
            print(' ')

    def printClients (self, siteName):
        getClientsUrl = f'api/s/{siteName}/stat/sta'
        url = f"https://{self.host}:{self.port}/{getClientsUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        pprint (response)
        api_data = response.json()
        responseList = api_data['data']
        for r in responseList:
            print (f"Client: {r['hostname']}")
            print (f"Signal: {r['signal']}")
            print (f"Noise: {r['noise']}")

    def getSiteName (self, desc):
        # Set up to get site name
        getSitesUrl = 'api/self/sites'
        url = f"https://{self.host}:{self.port}/{getSitesUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        api_data = response.json()
        # print("/" * 50)
        # pprint(api_data)
        # print("/" * 50)

        # Parse out the resulting list of
        responseList = api_data['data']
        # pprint(responseList)

        n = 'name'
        for items in responseList:
            if items.get('desc') == desc:
                return items.get('name')

        return n
