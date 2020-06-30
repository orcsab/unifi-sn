# From https://github.com/DataKnox/CodeSamples

import getpass
from pprint import pprint

from unifi import Unifi
from sn import ServiceNow

unifiAdmin = 'api' # a read only admin account I created on the controller
unifiPass = getpass.getpass(prompt='Unifi Password: ', stream=None)

snAdmin = 'admin'
snPass = getpass.getpass(prompt='ServiceNow Password: ', stream=None)
snTable = 'x_snc_home_wifi_clients'

# Fetch all active clients from my home Wifi.
controller = Unifi("raspberrypi.local", 8443, unifiAdmin, unifiPass)
name = controller.getSiteName("SingHonk")
activeClients = controller.getClients(name)
print ('ACTIVE CLIENTS')
pprint (activeClients)

# Get the last recording of active clients from the wifi client table in my
# instance.
sn = ServiceNow ('https://drummonds.service-now.com', snAdmin, snPass)
ledger = sn.getRecords(snTable)

print ('LEDGER')
pprint (ledger)

# This loop will add to the table (ledger) any active clients that it does
# not know about. It will also record time series in MetricBase for each
# active client.
for c in activeClients:
    sysId = 0
    for item in ledger:
        if item['id'] == c['_id']:
            sysId = item['sys_id']

    if sysId == 0:
        r = {
            "id": c['_id'],
            "name": c['hostname']
        }
        print (f'adding new active device to {snTable}: {c["hostname"]}')
        newRecord = sn.addRecord ('x_snc_home_wifi_clients', r)
        sysId = newRecord['sys_id']

    metrics = ['noise', 'signal', 'latest_assoc_time', 'satisfaction', 'assoc_time']
    for m in metrics:
        print (f'addMetric for {c["hostname"]}: {snTable}, {sysId}, {m}, {c[m]}')
        sn.addMetric(snTable, sysId, m, c[m])
