#!/usr/bin/env python

import sys
import aux, INF1822
from omniORB import CORBA

# ==================================================
#
#	Master
#
# ==================================================

# ORB setup
orbManager = aux.ORBManager()
orbManager.initializePoa()
orbManager.activatePoa()

# Initializing the naming service
catalogueIor = aux.readIorFromFile("naming-service-ior.txt")
catalogue = orbManager.getStubFrom(catalogueIor, INF1822.Catalogue)
if catalogue is None:
	print("Error with catalogue reference")
	sys.exit(1)

# Registering the master light device in the catalogue
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

# Real program (starts monitoring the other devices
# and updates the global light)
masterServant.start()
