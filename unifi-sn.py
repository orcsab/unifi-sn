# From https://github.com/DataKnox/CodeSamples

import requests
import json
from pprint import pprint
import urllib3
import getpass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up connection parameters in a dictionary
gateway = {"ip": "raspberrypi.local", "port": "8443"}

username = 'api'
password = getpass.getpass(prompt='Password: ', stream=None)

# set REST API headers
headers = {"Accept": "application/json",
           "Content-Type": "application/json"}
# set URL parameters
loginUrl = 'api/login'
url = f"https://{gateway['ip']}:{gateway['port']}/{loginUrl}"
# set username and password
body = {
    "username": username,
    "password": password
}
# Open a session for capturing cookies
session = requests.Session()
# login
response = session.post(url, headers=headers,
                        data=json.dumps(body), verify=False)

# parse response data into a Python object
api_data = response.json()
print("/" * 50)
pprint(api_data)
print('Logged in!')
print("/" * 50)

# Set up to get site name
getSitesUrl = 'api/self/sites'
url = f"https://{gateway['ip']}:{gateway['port']}/{getSitesUrl}"
response = session.get(url, headers=headers,
                       verify=False)
api_data = response.json()
print("/" * 50)
pprint(api_data)
print("/" * 50)

# Parse out the resulting list of
responseList = api_data['data']
pprint(responseList)

n = 'name'
for items in responseList:
    if items.get('desc') == 'SingHonk':
        n = items.get('name')
# print(n)

getDevicesUrl = f"api/s/{n}/stat/device"
url = f"https://{gateway['ip']}:{gateway['port']}/{getDevicesUrl}"
response = session.get(url, headers=headers,
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

getClientsUrl = f'api/s/{n}/stat/sta'
url = f"https://{gateway['ip']}:{gateway['port']}/{getClientsUrl}"
response = session.get(url, headers=headers,
                       verify=False)
pprint (response)
api_data = response.json()
responseList = api_data['data']
for r in responseList:
    print (f"Client: {r['hostname']}")
    print (f"Signal: {r['signal']}")
    print (f"Noise: {r['noise']}")
