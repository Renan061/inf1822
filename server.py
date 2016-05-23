#!/usr/bin/env python

import sys
import aux, INF1822

# ==================================================
#
#	Server
#
# ==================================================

print "Server started..."

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
masterServant = aux.MasterLightDeviceImpl(orbManager, 1, "master")
masterIor = orbManager.getIorFrom(masterServant)
ok = catalogue.register(masterIor, "master", INF1822.MasterLightDeviceType) # TODO: Device name
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
		print "Device light level is " + str(device.lightLevel)

print "Server finished..."
