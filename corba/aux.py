
import sys
from omniORB import CORBA, PortableServer
import INF1822, INF1822__POA
import time, threading

# ==================================================
#
#	IDL Implementations
#
# ==================================================

class MasterLightDeviceImpl(INF1822__POA.MasterLightDevice):
	# Default constructor
	def __init__(self, orbManager, id, type):
		self._orbManager = orbManager
		self._deviceList = []
		self._lock = threading.Lock()
		self.id = id
		self.type = type
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
			print("Registered devices used to calculate the global light level: [" + value + "]")
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

class LightDeviceImpl(INF1822__POA.LightDevice):
	# Default constructor
	def __init__(self, id, type, values):
		self.id = id
		self.type = type
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
#	ORBManager
#
# ==================================================

class ORBManager:
	# Default constructor
	def __init__(self):
		self._orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

	def initializePoa(self):
		self._poa = self._orb.resolve_initial_references("RootPOA")

	def activatePoa(self):
		self._poa._get_the_POAManager().activate()

	def runOrb(self):
		self._orb.run()

	# TODO: Should this return an error
	def getIorFrom(self, objectServant):
		objectReference = objectServant._this()
		return self._orb.object_to_string(objectReference)

	def getStubFrom(self, objectIor, objectClass):
		objectReference = self._orb.string_to_object(objectIor)
		return objectReference._narrow(objectClass)

# ==================================================
#
#	Auxiliary functions
#
# ==================================================

def readIorFromFile(filename):
	with open(filename, "r") as file:
		ior = file.read()
	return ior

def writeIorToFile(ior, filename):
	with open(filename, "w") as file:
		file.write(ior)
