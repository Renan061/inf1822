
import sys
from omniORB import CORBA, PortableServer
import INF1822, INF1822__POA
import time, threading

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
