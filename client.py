#!/usr/bin/env python

import sys
import aux, INF1822, NamingService

# ==================================================
#
#	Client
#
# ==================================================

print "Client started..."

# Setup
orbManager = aux.ORBManager()
orbManager.initializePoa()

# Naming service
objectManagerIor = aux.readIorFromFile("naming-service-ior.txt")
objectManager = orbManager.getObjectFrom(objectManagerIor, NamingService.ObjectManager)
if objectManager is None:
	print("Error with object manager reference")
	sys.exit(1)


# MasterLightDevice
masterIor = objectManager.getByName("MasterLightDevice")
master = orbManager.getObjectFrom(masterIor, INF1822.MasterLightDevice)
if master is None:
	print("Error with master reference")
	sys.exit(1)

# LightDevice
lightDeviceServant = aux.LightDeviceImpl(2, "light", [120, 50, 140, 20, 100,
	90, 60, 80, 40, 110, 10, 150, 30, 130])
lightDeviceIor = orbManager.getIorFrom(lightDeviceServant)
ok = objectManager.register(lightDeviceIor, "LightDevice", "sensor");
if not ok:
	print("Error with registering of light device")
	sys.exit(1)

# Doing something
ok = master.startMonitoringDevice(lightDeviceIor)
if not ok:
	print("Error when starting to monitor a light device")
	sys.exit(1)
lightDeviceServant.start()

# Running
orbManager.activatePoa()
orbManager.runOrb()

print "Client finished..."
