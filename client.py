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

# Naming service
objectManagerIor = aux.readIorFromFile("naming-service-ior.txt")
objectManager = orbManager.getObjectFrom(objectManagerIor,
	NamingService.ObjectManager):
if objectManager is None:
	print "Error with object manager reference"
    sys.exit(1)


# MasterLightDevice
masterIor = objectManager.getByName("MasterLightDevice")
master = orbManager.getObjectFrom(masterIor,
	INF1822.MasterLightDevice):
if master is None:
    print "Error with master reference"
    sys.exit(1)

print(master.id)

# # LightDevice
# # Object implementation
# lightDeviceServant = LightDeviceServant(2, "light", [120, 50, 140, 20, 100,
# 	90, 60, 80, 40, 110, 10, 150, 30, 130])
# lightDevice = lightDeviceServant._this() # How does this work?

# # Bind the Device object to the test context
# name = [CosNaming.NameComponent("INF1822LightDevice" + str(lightDeviceServant.id), "Object")]
# try:
#     objectManager.context.bind(name, lightDevice)
#     print "New INF1822LightDevice object bound"
# except CosNaming.NamingContext.AlreadyBound:
#     objectManager.context.rebind(name, lightDevice)
#     print "INF1822LightDevice binding already existed -- rebound"

# # Activate the POA
# objectManager.poa._get_the_POAManager().activate()

# #
# # Doing something
# #
# master.startMonitoringDevice(lightDevice)
# lightDeviceServant.start()

# Run ORB
orbManager.runOrb()

print "Client finished..."
