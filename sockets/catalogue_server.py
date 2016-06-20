#!/usr/bin/env python

import socket
import threading

# ==================================================
#
#	Catalogue class
#
# ==================================================

class Catalogue:
	# Default constructor
	def __init__(self):
		self._clusterDictionary = {}
		self._masterIdDictionary = {}
		self._lock = threading.Lock()

	def register(self, deviceAddress, id, type, clusterId):
		if not isinstance(id, long) or not isinstance(clusterId, long):
			return False

		self._lock.acquire()
		if not self._clusterDictionary.has_key(clusterId):
			self._clusterDictionary[clusterId] = {}

		if not self._clusterDictionary[clusterId].has_key(type):
			self._clusterDictionary[clusterId][type] = {}

		if self._clusterDictionary[clusterId][type].has_key(id):
			self._lock.release()
			return False

		self._clusterDictionary[clusterId][type][id] = deviceAddress
		self._lock.release()

		print("Registered device <" + str(id) + "> in cluster <" + str(clusterId) + ">")
		return True

	def registerMaster(self, deviceAddress, id, type, clusterId):
		ok = self.register(deviceAddress, id, type, clusterId)

		if ok:
			self._lock.acquire()
			if not self._masterIdDictionary.has_key(clusterId):
				self._masterIdDictionary[clusterId] = {}
			self._masterIdDictionary[clusterId][type] = id
			self._lock.release()
			
		return ok

	def deregister(self, deviceAddress, id, type, clusterId):
		value = False
		self._lock.acquire()
		for clusterKey, typeDictionary in self._clusterDictionary.items():
			for typeKey, idDictionary in typeDictionary.items():
				if idDictionary.get(id) is deviceAddress:
					del self._clusterDictionary[clusterKey][typeKey][id]
					if len(idDictionary) is 0:
						del self._clusterDictionary[clusterKey][typeKey]
					if len(typeDictionary) is 0:
						del self._clusterDictionary[clusterKey]
					value = True
					print("Deregistered device <" + str(id) + "> in cluster <" + str(clusterId) + ">")
					break
		self._lock.release()
		return value

	def deregisterMaster(self, deviceAddress, id, type, clusterId):
		ok = self.deregister(deviceAddress, id, type, clusterId)

		if ok:
			self._lock.acquire()
			if self._masterIdDictionary.has_key(clusterId):
				del self._masterIdDictionary[clusterId]
			self._lock.release()

		return ok

	def getByType(self, type, clusterId):
		addressList = []
		self._lock.acquire()
		for _, deviceAddress in self._clusterDictionary[clusterId][type].items():
			addressList.append(deviceAddress)
		self._lock.release()
		return addressList

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

		value = idDictionary.get(self._masterIdDictionary[clusterId][type])
		self._lock.release()
		if value is None:
			return ""
		return value

# ==================================================
#
#	Parsing
#
# ==================================================

# ==================================================
#
#	Sockets
#
# ==================================================

# Setup
serverAddress = ("localhost", 1984)

# Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(5)

# Catalogue
catalogue = Catalogue()

print("New server on: " + str(serverAddress))

while True:
    # Accepts connections from outside
    (clientSocket, address) = serverSocket.accept()
    print("New connection with: " + str(address))

    # Does something with the clientSocket
    message = ""
    while True:
    	data = clientSocket.recv(4096)
    	if data:
    		message += data
    		print("Received: ", data)
    	else:
    		print("Stoped receiving...")
    		break
    print("Final message: " + message)

    clientSocket.close()
