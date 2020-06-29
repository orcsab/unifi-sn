# From https://github.com/DataKnox/CodeSamples

import getpass
from unifi import Unifi

username = 'api' # a read only admin account I created on the controller
password = getpass.getpass(prompt='Password: ', stream=None)

controller = Unifi("raspberrypi.local", 8443, username, password)
name = controller.getSiteName("SingHonk")
controller.printDevices(name)
controller.printClients(name)
