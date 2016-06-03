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
		self._typeDictionary = {}
		self._lock = threading.Lock()
		self._masterName = "master"

	def register(self, deviceIor, name, type):
		if not isinstance(deviceIor, basestring) or not isinstance(name, basestring):
			return False

		self._lock.acquire()
		if not self._typeDictionary.has_key(type):
			self._typeDictionary[type] = {}
		self._typeDictionary[type][name] = deviceIor
		self._lock.release()

		print("Registered <" + name + ">")
		return True

	def registerMaster(self, deviceIor, type):
		return self.register(deviceIor, self._masterName, type)

	def deregister(self, deviceIor, name):
		value = False
		self._lock.acquire()
		for key, nameDictionary in self._typeDictionary.items():
			if nameDictionary.get(name) is deviceIor:
				del nameDictionary[name]
				if len(nameDictionary) is 0:
					del self._typeDictionary[key]
				value = True
				print("Deregistered <" + name + ">")
				break
		self._lock.release()
		return value

	def deregisterMaster(self, deviceIor):
		return self.deregister(deviceIor, self._masterName)

	def getByName(self, name):
		value = ""
		self._lock.acquire()
		for key, nameDictionary in self._typeDictionary.items():
			if nameDictionary.has_key(name):
				value = nameDictionary[name]
				break
		self._lock.release()
		return value

	def getByType(self, type):
		iorList = []
		self._lock.acquire()
		for name, deviceIor in self._typeDictionary[type].items():
			iorList.append(deviceIor)
		self._lock.release()
		return iorList

	def getMasterForType(self, type):
		self._lock.acquire()
		nameDictionary = self._typeDictionary.get(type)

		if nameDictionary is None:
			self._lock.release()
			return ""

		value = nameDictionary.get(self._masterName)
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
aux.writeIorToFile(ior, "naming-service-ior.txt")

# Runnig
orbManager.activatePoa()
orbManager.runOrb()

print "Naming service finished..."
