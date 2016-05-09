#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import CosNaming, INF1822, INF1822__POA

# 
# Implementations
# 

class DeviceServant (INF1822__POA.Device):
	# Default constructor
	def __init__(self, id, type):
		self.id = id
		self.type = type

# 
# Server
# 

print "Server started..."

# ORB setup
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)
poa = orb.resolve_initial_references("RootPOA")

# Object implementation
deviceServant = DeviceServant(1132, "master")
device = deviceServant._this() # How does this work?

# Naming service
obj = orb.resolve_initial_references("NameService");
rootContext = obj._narrow(CosNaming.NamingContext)

if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Bind a context named "server.inf1822" to the root context
name = [CosNaming.NameComponent("server", "inf1822")]
try:
    testContext = rootContext.bind_new_context(name)
    print "New test context bound"
except CosNaming.NamingContext.AlreadyBound, ex:
    print "Test context already exists"
    obj = rootContext.resolve(name)
    testContext = obj._narrow(CosNaming.NamingContext)
    if testContext is None:
        print "server.inf1822 exists but is not a NamingContext"
        sys.exit(1)

# Bind the Device object to the test context
name = [CosNaming.NameComponent("INF1822Device", "Object")]
try:
    testContext.bind(name, device)
    print "New INF1822Device object bound"
except CosNaming.NamingContext.AlreadyBound:
    testContext.rebind(name, device)
    print "INF1822Device binding already existed -- rebound"

# Activate the POA and wait
poa._get_the_POAManager().activate()
orb.run()

print "Server finished..."
