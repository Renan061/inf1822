#!/usr/bin/env python

import sys, threading, time
import aux, INF1822
from omniORB import CORBA
import INF1822, INF1822__POA

# ==================================================
#
#	MasterLightDevice
#
# ==================================================

class MasterLightDeviceImpl(INF1822__POA.MasterLightDevice):
	# Default constructor
	def __init__(self, orbManager, id, type, clusterId):
		self._orbManager = orbManager
		self._deviceList = []
		self._lock = threading.Lock()
		self.id = id
		self.type = type
		self.clusterId = clusterId
		self.lightLevel = 0

	def startMonitoringDevice(self, deviceIor):
		device = self._orbManager.getStubFrom(deviceIor, INF1822.LightDevice)
		if device is None:
			return False
		self._lock.acquire()
		self._deviceList.append(device)
		self._lock.release()
		print("Started monitoring device " + str(device.id))
		return True

	def start(self):
		try:
			threading.Thread(target=self._monitor).start()
		except:
			print "Unable to start new thread"
		
	def _monitor(self):
		while True:
			deviceIdList = self._refreshGlobalLightLevel()
			value = "none" if len(deviceIdList) == 0 else ", ".join([str(i) for i in deviceIdList])
			print("====================")			
			print("Registered devices used to calculate the global " +
				"light level of cluster <" + str(self.clusterId) +
				">: [" + value + "]")
			print("Global light level: " + str(self.lightLevel))
			print("====================")
			time.sleep(5)

	def _refreshGlobalLightLevel(self):
		value = 0
		deviceIdList = [] # Only used for logging purposes (shouldn't be in production)

		self._lock.acquire()
		for device in self._deviceList:
			try:
				value += device.lightLevel
				deviceIdList.append(device.id)
			except (CORBA.TRANSIENT, CORBA.COMM_FAILURE):
				print("Could not get light level for one of the devices")
		deviceListLength = len(self._deviceList)
		self._lock.release()

		if deviceListLength != 0:
			self.lightLevel = value / deviceListLength
		return deviceIdList

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
masterServant = MasterLightDeviceImpl(orbManager, deviceId,
	INF1822.MasterLightDeviceType, clusterId)
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
