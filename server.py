#!/usr/bin/env python

import sys
import aux, INF1822, NamingService

# ==================================================
#
#	Server
#
# ==================================================

print "Server started..."

# ORB setup
orbManager = aux.ORBManager()
orbManager.initializePoa()

# Naming service
objectManagerIor = aux.readIorFromFile("naming-service-ior.txt")
objectManager = orbManager.getObjectFrom(objectManagerIor, NamingService.ObjectManager)
if objectManager is None:
	print("Error with object manager reference")
	sys.exit(1)

# MasterLightDevice
masterServant = aux.MasterLightDeviceImpl(orbManager, 1, "master")
masterIor = orbManager.getIorFrom(masterServant)
ok = objectManager.register(masterIor, "MasterLightDevice", "master");
if not ok:
	print("Error with registering of master light device")
	sys.exit(1)

# POA
orbManager.activatePoa()

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

# orbManager.runOrb()

print "Server finished..."
