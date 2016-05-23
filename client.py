#!/usr/bin/env python

import sys
import aux, INF1822

# ==================================================
#
#	Client
#
# ==================================================

print "Client started..."

# Setup
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
masterIor = catalogue.getByName("master")
master = orbManager.getStubFrom(masterIor, INF1822.MasterLightDevice)
if master is None:
	print("Error with master reference")
	sys.exit(1)

# LightDevice
lightDeviceServant = aux.LightDeviceImpl(2, INF1822.LightDeviceType, [120, 50,
	140, 20, 100, 90, 60, 80, 40, 110, 10, 150, 30, 130])
lightDeviceIor = orbManager.getIorFrom(lightDeviceServant)
ok = catalogue.register(lightDeviceIor, "light", INF1822.LightDeviceType);
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
orbManager.runOrb()

print "Client finished..."
