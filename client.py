#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import CosNaming, INF1822, INF1822__POA
import time, threading

# ==================================================
#
#	Implementations
#
# ==================================================

class LightDeviceServant(INF1822__POA.LightDevice):
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
			print "Valor de luminosidade lido: " + str(value)
			self.index += 1
			self.index = 0 if self.index == len(self.values) - 1 else self.index + 1

			time.sleep(1)

# ==================================================
#
#	Internal
#
# ==================================================

class ObjectManager:
	# Default constructor
	def __init__(self):
		# ORB setup
		self.orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
		self.poa = self.orb.resolve_initial_references("RootPOA")

		# Obtain a reference to the root naming context
		obj = self.orb.resolve_initial_references("NameService")
		self.rootContext = obj._narrow(CosNaming.NamingContext)
		if self.rootContext is None:
		    print "Failed to narrow the root naming context"
		    sys.exit(1)

		# Bind a context named "server.inf1822" to the root context
		name = [CosNaming.NameComponent("server", "inf1822")]
		try:
		    self.context = self.rootContext.bind_new_context(name)
		    print "New context bound"
		except CosNaming.NamingContext.AlreadyBound, ex:
		    print "Context already exists"
		    obj = self.rootContext.resolve(name)
		    self.context = obj._narrow(CosNaming.NamingContext)
		    if self.context is None:
		        print "server.inf1822 exists but is not a NamingContext"
		        sys.exit(1)

	def getStub(self):
		print "Get Stub"

	def publishSkeleton(self):
		print "Publish Skeleton"

# ==================================================
#
#	Client
#
# ==================================================

print "Client started..."

objectManager = ObjectManager()

#
# MasterLightDevice
#

# Resolve the name "server.inf1822/INF1822Device.Object"
name = [CosNaming.NameComponent("server", "inf1822"),
        CosNaming.NameComponent("INF1822MasterLightDevice", "Object")]
try:
    obj = objectManager.rootContext.resolve(name)
except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an INF1822::MasterLightDevice
master = obj._narrow(INF1822.MasterLightDevice)
if master is None:
    print "Object reference is not an INF1822::MasterLightDevice"
    sys.exit(1)

#
# LightDevice
#

# Object implementation
lightDeviceServant = LightDeviceServant(2, "light", [120, 50, 140, 20, 100,
	90, 60, 80, 40, 110, 10, 150, 30, 130])
lightDevice = lightDeviceServant._this() # How does this work?

# Bind the Device object to the test context
name = [CosNaming.NameComponent("INF1822LightDevice" + str(lightDeviceServant.id), "Object")]
try:
    objectManager.context.bind(name, lightDevice)
    print "New INF1822LightDevice object bound"
except CosNaming.NamingContext.AlreadyBound:
    objectManager.context.rebind(name, lightDevice)
    print "INF1822LightDevice binding already existed -- rebound"

# Activate the POA
objectManager.poa._get_the_POAManager().activate()

#
# Doing something
#
master.startMonitoringDevice(lightDevice)
lightDeviceServant.start()

# Run ORB
objectManager.orb.run()

print "Client finished..."
