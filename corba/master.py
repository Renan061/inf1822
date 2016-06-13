#!/usr/bin/env python

import sys
import aux, INF1822
from omniORB import CORBA

# ==================================================
#
#	Master
#
# ==================================================

# Checking for parameters
if len(sys.argv) != 3:
	print "First parameter must be clusterId and second parameter must be deviceId..."
	sys.exit(1)
clusterId = int(sys.argv[1])
deviceId = int(sys.argv[2])

# ORB setup
orbManager = aux.ORBManager()
orbManager.initializePoa()
orbManager.activatePoa()

# Initializing the naming service
catalogueIor = aux.readIorFromFile("catalogue-ior.txt")
catalogue = orbManager.getStubFrom(catalogueIor, INF1822.Catalogue)
if catalogue is None:
	print("Error with catalogue reference")
	sys.exit(1)

# Registering the master light device in the catalogue
masterServant = aux.MasterLightDeviceImpl(orbManager, deviceId,
	INF1822.MasterLightDeviceType)
masterIor = orbManager.getIorFrom(masterServant)
try:
	ok = catalogue.registerMaster(masterIor, masterServant.id,
		INF1822.LightDeviceType, clusterId)
except:
	print("Error catalogue.registerMaster (CORBA Exception)")
	sys.exit(1)
if not ok:
	print("Error with registering of master light device")
	sys.exit(1)

# Real program (starts monitoring the other devices
# and updates the global light)
masterServant.start()
