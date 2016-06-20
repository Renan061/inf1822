#!/usr/bin/env python

import sys, threading, time
import aux, INF1822
from omniORB import CORBA
import INF1822, INF1822__POA

# ==================================================
#
#	LightDevice
#
# ==================================================

class LightDeviceImpl(INF1822__POA.LightDevice):
	# Default constructor
	def __init__(self, id, type, clusterId, values):
		self.id = id
		self.type = type
		self.clusterId = clusterId
		self.lightLevel = 0
		self.values = values
		self.index = 0

	# Starts a new thread
	def start(self):
		try:
			threading.Thread(target=self._listen).start()
		except:
			print "Unable to start new thread"

	# Stub
	def _listen(self):
		while True:
			value = self.values[self.index]
			self.lightLevel = value
			# print "Device " + str(self.id) + " - Valor de luminosidade lido: " + str(value)
			self.index = 0 if self.index == len(self.values) - 1 else self.index + 1
			time.sleep(1)

# ==================================================
#
#	Client
#
# ==================================================

# Checking for parameters
if len(sys.argv) != 3:
	print "First parameter must be clusterId and second parameter must be deviceId..."
	sys.exit(1)
clusterId = int(sys.argv[1])
deviceId = int(sys.argv[2])

# Setup - ORB and light device servant
orbManager = aux.ORBManager()
orbManager.initializePoa()
orbManager.activatePoa()
lightDeviceServant = LightDeviceImpl(deviceId, INF1822.LightDeviceType,
	clusterId, [10, 20, 30, 40, 30, 20])

# Initializing the naming service
catalogueIor = aux.readIorFromFile("catalogue-ior.txt")
catalogue = orbManager.getStubFrom(catalogueIor, INF1822.Catalogue)
if catalogue is None:
	print("Error with catalogue reference")
	sys.exit(1)

# Getting the master from the catalogue
try:
	masterIor = catalogue.getMasterForType(lightDeviceServant.type, clusterId)
except:
	print("Error catalogue.getMasterForType (CORBA Exception)")
	sys.exit(1)
if not masterIor:
	print("Error master not registered")
	sys.exit(1)
master = orbManager.getStubFrom(masterIor, INF1822.MasterLightDevice)
if not master:
	print("Error with master reference")
	sys.exit(1)

# Registering the light device in the catalogue
lightDeviceIor = orbManager.getIorFrom(lightDeviceServant)
try:
	ok = catalogue.register(lightDeviceIor, lightDeviceServant.id,
		INF1822.LightDeviceType, clusterId);
except:
	print("Error catalogue.register (CORBA Exception)")
	sys.exit(1)
if not ok:
	print("Error with registering of light device")
	sys.exit(1)

# Telling the master to start monitoring the device
lightDeviceServant.start()
try:
	ok = master.startMonitoringDevice(lightDeviceIor)
except:
	print("Error master.startMonitoringDevice (CORBA Exception)")
	sys.exit(1)
if not ok:
	print("Error when starting to monitor a light device")
	sys.exit(1)

# Running
orbManager.runOrb()

print "Client finished..."
