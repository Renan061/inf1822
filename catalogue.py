#!/usr/bin/env python

import aux
import INF1822, INF1822__POA
import threading

# ==================================================
#
#	Implementations
#
# ==================================================

class CatalogueImpl(INF1822__POA.Catalogue):
	# Default constructor
	def __init__(self):
		self._clusterDictionary = {}
		self._lock = threading.Lock()
		self._masterId = 0

	def register(self, deviceIor, id, type, clusterId):
		if not isinstance(deviceIor, basestring) or not isinstance(id, long):
			return False

		self._lock.acquire()
		if not self._clusterDictionary.has_key(clusterId):
			self._clusterDictionary[clusterId] = {}

		if not self._clusterDictionary[clusterId].has_key(type):
			self._clusterDictionary[clusterId][type] = {}

		if self._clusterDictionary[clusterId][type].has_key(id):
			self._lock.release()
			return False

		self._clusterDictionary[clusterId][type][id] = deviceIor
		self._lock.release()

		print("Registered device with id <" + id + ">")
		return True

	def registerMaster(self, deviceIor, type, clusterId):
		# NOTE: If there was another master, this would fail.
		# Should force rewriting when registering another master.
		return self.register(deviceIor, self._masterId, type, clusterId)

	def deregister(self, deviceIor, id, type, clusterId):
		value = False
		self._lock.acquire()
		for clusterKey, typeDictionary in self._clusterDictionary.items():
			for typeKey, idDictionary in typeDictionary.items():
				if idDictionary.get(id) is deviceIor:
					del self._clusterDictionary[clusterKey][typeKey][id]
					if len(idDictionary) is 0:
						del self._clusterDictionary[clusterKey][typeKey]
					if len(typeDictionary) is 0:
						del self._clusterDictionary[clusterKey]
					value = True
					print("Deregistered device with id <" + id + ">")
					break
		self._lock.release()
		return value

	def deregisterMaster(self, deviceIor, type, clusterId):
		return self.deregister(deviceIor, self._masterId, type, clusterId)

	def getByType(self, type, clusterId):
		iorList = []
		self._lock.acquire()
		for _, deviceIor in self._clusterDictionary[clusterId][type].items():
			iorList.append(deviceIor)
		self._lock.release()
		return iorList

	def getMasterForType(self, type, clusterId):
		self._lock.acquire()

		typeDictionary = self._clusterDictionary.get(clusterId)
		if typeDictionary is None:
			self._lock.release()
			return ""

		idDictionary = typeDictionary.get(type)
		if idDictionary is None:
			self._lock.release()
			return ""

		value = idDictionary.get(self._masterName)
		self._lock.release()
		if value is None:
			return ""
		return value

# ==================================================
#
#	Main
#
# ==================================================

print "Naming service started..."

# Starting
orbManager = aux.ORBManager()
orbManager.initializePoa()

# Doing stuff
catalogueServant = CatalogueImpl()
ior = orbManager.getIorFrom(catalogueServant)
aux.writeIorToFile(ior, "catalogue-ior.txt")

# Runnig
orbManager.activatePoa()
orbManager.runOrb()

print "Naming service finished..."
