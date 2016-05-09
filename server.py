#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import CosNaming, INF1822, INF1822__POA

# ==================================================
#
#	Implementations
#
# ==================================================

class MasterLightDeviceServant(INF1822__POA.MasterLightDevice):
	# Default constructor
	def __init__(self, id, type):
		self.id = id
		self.type = type
		self.lightLevel = -1
		self._deviceList = []

	def startMonitoringDevice(self, device):
		print "Started monitoring device " + str(device.id)
		self._deviceList.append(device)
		print self._deviceList

	def getDeviceForId(self, id):
		for device in self._deviceList:
			if device.id == id:
				return device
		return None

# ==================================================
#
#	Server
#
# ==================================================

print "Server started..."

# ORB setup
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Naming service
obj = orb.resolve_initial_references("NameService");
rootContext = obj._narrow(CosNaming.NamingContext)
if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Bind a context named "server.inf1822" to the root context
name = [CosNaming.NameComponent("server", "inf1822")]
try:
    testContext = rootContext.bind_new_context(name)
    print "New test context bound"
except CosNaming.NamingContext.AlreadyBound, ex:
    print "Test context already exists"
    obj = rootContext.resolve(name)
    testContext = obj._narrow(CosNaming.NamingContext)
    if testContext is None:
        print "server.inf1822 exists but is not a NamingContext"
        sys.exit(1)

# Object implementation
masterServant = MasterLightDeviceServant(1, "master")
master = masterServant._this() # How does this work?

# Bind the Device object to the test context
name = [CosNaming.NameComponent("INF1822MasterLightDevice", "Object")]
try:
    testContext.bind(name, master)
    print "New INF1822MasterLightDevice object bound"
except CosNaming.NamingContext.AlreadyBound:
    testContext.rebind(name, master)
    print "INF1822MasterLightDevice binding already existed -- rebound"

# Activate the POA
poa._get_the_POAManager().activate()

#
# Real program
#
while True:
	value = input("Device ID: ")
	if value == -1:
		break
	device = masterServant.getDeviceForId(value)
	if device is None:
		print "Device with id " + str(value) + " not found"
	else:
		print "Device light level is " + str(device.lightLevel)

print "Server finished..."
