# From https://github.com/DataKnox/CodeSamples

import getpass
from pprint import pprint

from unifi import Unifi
from sn import ServiceNow

unifiAdmin = 'api' # a read only admin account I created on the controller
unifiPass = getpass.getpass(prompt='Unifi Password: ', stream=None)

snAdmin = 'admin'
snPass = getpass.getpass(prompt='ServiceNow Password: ', stream=None)

controller = Unifi("raspberrypi.local", 8443, unifiAdmin, unifiPass)
name = controller.getSiteName("SingHonk")
controller.printDevices(name)
controller.printClients(name)

sn = ServiceNow ('https://drummonds.service-now.com', snAdmin, snPass)
records = sn.getRecords('u_fridge')
pprint (records)
