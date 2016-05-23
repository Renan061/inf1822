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

	def register(self, ior, name, type):
		if not isinstance(ior, basestring) or not isinstance(name, basestring):
			return False

		self._lock.acquire()
		if not self._typeDictionary.has_key(type):
			self._typeDictionary[type] = {}
		self._typeDictionary[type][name] = ior
		self._lock.release()

		print("Registered <" + name + ">")
		return True

	def deregister(self, ior, name):
		value = False
		self._lock.acquire()
		for key, nameDictionary in self._typeDictionary.items():
			if nameDictionary.get(name) is ior:
				del nameDictionary[name]
				if len(nameDictionary) is 0:
					del self._typeDictionary[key]
				value = True
				break
		self._lock.release()
		return value

	def getByName(self, name):
		value = None
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
		for name, ior in self._typeDictionary[type].items():
			iorList.append(ior)
		self._lock.release()
		return iorList

	def getMasterForType(self, type):
		self._lock.acquire()
		nameDictionary = self._typeDictionary.get(type)
		
		if nameDictionary is None:
			self._lock.release()
			return None

		value = nameDictionary.get("master")
		self._lock.release()
		return value # TODO

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
