# From https://github.com/DataKnox/CodeSamples

import getpass
from pprint import pprint

from unifi import Unifi
from sn import ServiceNow

unifiAdmin = 'api' # a read only admin account I created on the controller
unifiPass = getpass.getpass(prompt='Unifi Password: ', stream=None)

snAdmin = 'admin'
snPass = getpass.getpass(prompt='ServiceNow Password: ', stream=None)

# Fetch all active clients from my home Wifi.
controller = Unifi("raspberrypi.local", 8443, unifiAdmin, unifiPass)
name = controller.getSiteName("SingHonk")
activeClients = controller.getClients(name)
print ('ACTIVE CLIENTS')
pprint (activeClients)

# Get the last recording of active clients from the wifi client table in my
# instance.
sn = ServiceNow ('https://drummonds.service-now.com', snAdmin, snPass)
ledger = sn.getRecords('x_snc_home_wifi_clients')

print ('LEDGER')
pprint (ledger)

# This loop will add to the table (ledger) any active clients that it does
# not know about. It will also record time series in MetricBase for each
# active client.
for c in activeClients:
    found = 0
    for item in ledger:
        if item['id'] == c['_id']:
            found = 1

    if found == 0:
        r = {
            "id": c['_id'],
            "name": c['hostname']
        }
        print (f'adding record {r}')
        sn.addRecord ('x_snc_home_wifi_clients', r)
