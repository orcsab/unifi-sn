# From https://github.com/DataKnox/CodeSamples

import getpass
import datetime

from unifi import Unifi
from sn import ServiceNow

# Fetch all active clients from my home Wifi.
controller = Unifi('unifi.cfg')
name = controller.getSiteName("SingHonk")
activeClients = controller.getClients(name)
timestamp = datetime.datetime.utcnow().replace(microsecond=0).isoformat()

# Get the last recording of active clients from the wifi client table in my
# instance.
sn = ServiceNow ('sn.cfg')
snTable = 'x_snc_home_wifi_clients'
ledger = sn.getRecords('x_snc_home_wifi_clients')

# This loop will add to the table (ledger) any active clients that it does
# not know about. It will also record time series in MetricBase for each
# active client.
for c in activeClients:
    sysId = 0
    for item in ledger:
        if item['id'] == c['_id']:
            sysId = item['sys_id']

    if sysId == 0:
        # Debugging hopefully. Sometimes I get a strange client that seems to lack
        # a host name.
        if 'hostname' not in c:
            raise Exception (f'no hostname in client: {c}')

        r = {
            "id": c['_id'],
            "name": c['hostname']
        }
        print (f'adding new active device to {snTable}: {c["hostname"]}')
        newRecord = sn.addRecord (snTable, r)
        sysId = newRecord['sys_id']

    metrics = ['noise', 'signal', 'latest_assoc_time', 'satisfaction', 'assoc_time']
    for m in metrics:
        print (f'addMetric for {c["hostname"]}: {snTable}, {sysId}, {m}, {c[m]}, {timestamp}')
        sn.addMetric(snTable, sysId, m, c[m], timestamp)
