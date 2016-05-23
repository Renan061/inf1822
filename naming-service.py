#!/usr/bin/env python

import aux
import INF1822, INF1822__POA

# ==================================================
#
#	Implementations
#
# ==================================================

class CatalogueImpl(INF1822__POA.Catalogue):
	# Default constructor
	def __init__(self):
		self._dictionary = {}

	def register(self, ior, name, type):
		# Check if name is string
		# Check if ior is string
		if self._dictionary.has_key(name):
			# FIXME: Return more information
			# return False
			return True
		self._dictionary[name] = ior
		# TODO: Do something with type
		print("Registered <" + name + ">")
		return True

	def deregister(self, ior, name):
		# TODO
		print("CatalogueImpl deregister")
		return False

	def getByName(self, name):
		if self._dictionary.has_key(name):
			return self._dictionary[name]
		return "error"

	def getByType(self, type):
		# TODO
		print("CatalogueImpl getByType")
		return ["not", "-", "implemented"]

	def getMasterForType(self, type):
		# TODO
		print("CatalogueImpl getMasterForType")
		return "not-implemented"

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
