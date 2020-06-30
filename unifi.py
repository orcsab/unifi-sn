# First learned this from From https://github.com/DataKnox/CodeSamples
# Additional API info at https://ubntwiki.com/products/software/unifi-controller/api

import requests
import json
import os
import configparser

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


    # Constructor
    # Build the connection to the Unifi controller specified in the passed config
    # file with credentials in the same. Note that some online docs I read said the ui.com
    # credentials won't work. So I created a separate admin account.
    def __init__ (self, cfgfile):
        if not os.path.isfile(cfgfile):
            raise Exception (f'__init__: no such file: {cfgfile}')

        config = configparser.ConfigParser()
        config.read(cfgfile)

        self.body = {
            "username": config['credentials']['name'],
            "password": config['credentials']['pass']
        }
        self.host = config['controller']['hostname']
        self.port = config['controller']['port']

        # Open a session for capturing cookies
        self.session = requests.Session()
        # login
        loginUrl = 'api/login'
        url = f"https://{self.host}:{self.port}/{loginUrl}"
        response = self.session.post(url, headers=self.headers,
                                data=json.dumps(self.body), verify=False)
        if response.status_code != 200:
            raise Exception(f'__init__ failed with code {response.status_code}: {response}')

        # parse response data into a Python object
        api_data = response.json()
        # print("/" * 50)
        # pprint(api_data)
        # print('Logged in!')
        # print("/" * 50)

    # printDevices
    # Prints all APs on the home network. A useless relic of early development
    # where I was seeing what data could be pulled.
    def printDevices (self, siteName):
        getDevicesUrl = f"api/s/{siteName}/stat/device"
        url = f"https://{self.host}:{self.port}/{getDevicesUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        if response.status_code != 200:
            raise Exception(f'printDevices failed with code {response.status_code}: {response}')

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

    # getClients
    # Get all clients connected on the site. Includes a parameter to search
    # for a subset of specific clients. But I've not tested that yet.
    def getClients (self, siteName, id = ''):
        getClientsUrl = f'api/s/{siteName}/stat/sta'
        url = f"https://{self.host}:{self.port}/{getClientsUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        if response.status_code != 200:
            raise Exception(f'getClients failed with code {response.status_code}: {response}')

        api_data = response.json()
        responseList = api_data['data']
        reply = []
        for r in responseList:
            if id != '' and r['_id'] == id:
                reply.append(r)
            elif id == '':
                reply.append(r)

        return reply

    # getSiteName
    # Get the site name from the description. TBH this confuses me because in
    # the controller I have this desciption screen in the field called "site name".
    # But somehow I've seen that even with that unique description the actual
    # site name is still "default".
    def getSiteName (self, desc):
        # Set up to get site name
        getSitesUrl = 'api/self/sites'
        url = f"https://{self.host}:{self.port}/{getSitesUrl}"
        response = self.session.get(url, headers=self.headers,
                               verify=False)
        if response.status_code != 200:
            raise Exception(f'getSiteName failed with code {response.status_code}: {response}')

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
