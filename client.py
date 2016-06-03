#!/usr/bin/env python

import sys
import aux, INF1822
from omniORB import CORBA

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
lightDeviceServant = aux.LightDeviceImpl(2, INF1822.LightDeviceType, [10, 20,
	30, 40])

# Naming service
catalogueIor = aux.readIorFromFile("naming-service-ior.txt")
catalogue = orbManager.getStubFrom(catalogueIor, INF1822.Catalogue)
if catalogue is None:
	print("Error with catalogue reference")
	sys.exit(1)

# MasterLightDevice
masterIor = catalogue.getMasterForType(lightDeviceServant.type)
if not masterIor:
	print("Error master not registered")
	sys.exit(1)
master = orbManager.getStubFrom(masterIor, INF1822.MasterLightDevice)

# LightDevice
lightDeviceIor = orbManager.getIorFrom(lightDeviceServant)
lightDeviceName = "light" + str(lightDeviceServant.id)
try:
	ok = catalogue.register(lightDeviceIor, lightDeviceName, INF1822.LightDeviceType);
except CORBA.TRANSIENT:
	print("Error catalogue.register (CORBA.TRANSIENT)")
	sys.exit(1)
if not ok:
	print("Error with registering of light device")
	sys.exit(1)

if not master:
	print("Error with master reference")
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
