#!/usr/bin/env python
#coding=utf-8

import aux
import NamingService, NamingService__POA

# ==================================================
#
#	Implementations
#
# ==================================================

class ObjectManagerImpl(NamingService__POA.ObjectManager):
	# Default constructor
	def __init__(self):
		self.__dictionary = {}

	# Usado por um objeto para se registrar junto ao serviço.
	# Pode retornar false caso algum erro tenha ocorrido.
	def register(self, ior, name, type):
		# Check if name is string
		# Check if ior is string
		if self.__dictionary.has_key(name):
			# FIXME: Return more information
			# return False
			return True
		self.__dictionary[name] = ior
		# TODO: Do something with type
		print("Registered <" + name + "> of type <" + type +">")
		return True

	# Usado por um objeto para se desregistrar junto ao serviço.
	# Pode retornar false caso algum erro tenha ocorrido.
	def deregister(self, ior, name):
		# TODO
		print("ObjectManagerImpl deregister")
		return False

	# Retorna o IOR de um objeto dado seu nome.
	# Pode retornar um erro caso o objeto não exista.
	def getByName(self, name):
		if self.__dictionary.has_key(name):
			return self.__dictionary[name]
		return "error"

	# Retorna uma lista de IORs de objetos registrados pertencentes
	# ao tipo passado. Pode retornar uma lista vazia.
	def getByType(self, type):
		# TODO
		print("ObjectManagerImpl getByType")
		return ["not", "-", "implemented"]

	# Retorna o IOR de um objeto que é o "master" de seu tipo. 
	# Pode retornar um erro caso o objeto não exista.
	def getMasterForType(self, type):
		# TODO
		print("ObjectManagerImpl getMasterForType")
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
objectManagerServant = ObjectManagerImpl()
ior = orbManager.getIorFrom(objectManagerServant)
aux.writeIorToFile(ior, "naming-service-ior.txt")

# Runnig
orbManager.activatePoa()
orbManager.runOrb()

print "Naming service finished..."
