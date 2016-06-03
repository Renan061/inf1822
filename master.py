#!/usr/bin/env python

import sys
import aux, INF1822
from omniORB import CORBA

# ==================================================
#
#	Master
#
# ==================================================

print "Master started..."

# ORB setup
orbManager = aux.ORBManager()
orbManager.initializePoa()
orbManager.activatePoa()

# Naming service
catalogueIor = aux.readIorFromFile("naming-service-ior.txt")
catalogue = orbManager.getStubFrom(catalogueIor, INF1822.Catalogue)
if catalogue is None:
	print("Error with catalogue reference")
	sys.exit(1)

# MasterLightDevice
masterServant = aux.MasterLightDeviceImpl(orbManager, 1, INF1822.MasterLightDeviceType)
masterIor = orbManager.getIorFrom(masterServant)
try:
	ok = catalogue.registerMaster(masterIor, INF1822.LightDeviceType)
except CORBA.TRANSIENT:
	print("Error catalogue.registerMaster (CORBA.TRANSIENT)")
	sys.exit(1)
if not ok:
	print("Error with registering of master light device")
	sys.exit(1)

# Real program
while True:
	value = input("Device ID: ")
	if value == -1:
		break
	device = masterServant.getDeviceForId(value)
	if device is None:
		print "Device with id " + str(value) + " not found"
	else:
		try:
			print "Device light level is " + str(device.lightLevel)
		except CORBA.TRANSIENT:
			print("Error device.lightLevel (CORBA.TRANSIENT)")

ok = catalogue.deregisterMaster(masterIor, masterServant.type)
if not ok:
	print("Error with deregistering of master light device")

print "Master finished..."
