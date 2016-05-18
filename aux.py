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
		self.__orbManager = orbManager
		self.__deviceList = []
		self.id = id
		self.type = type
		self.lightLevel = -1

	def startMonitoringDevice(self, deviceIor):
		device = self.__orbManager.getObjectFrom(deviceIor, INF1822.LightDevice)
		if device is None:
			return False
		self.__deviceList.append(device)
		print "Started monitoring device"
		return True

	def getDeviceForId(self, id):
		for device in self.__deviceList:
			if device.id == id:
				return device
		return None

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
			print "Valor de luminosidade lido: " + str(value)
			self.index += 1
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
		self.__orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

	def initializePoa(self):
		self.__poa = self.__orb.resolve_initial_references("RootPOA")

	def activatePoa(self):
		self.__poa._get_the_POAManager().activate()

	def runOrb(self):
		self.__orb.run()

	# TODO: Should this return an error
	def getIorFrom(self, objectServant):
		objectReference = objectServant._this()
		return self.__orb.object_to_string(objectReference)

	def getObjectFrom(self, objectIor, objectClass):
		objectReference = self.__orb.string_to_object(objectIor)
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
