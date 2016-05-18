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

# Running
orbManager.activatePoa()
orbManager.runOrb()

print "Server finished..."
