#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import INF1822, INF1822__POA

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

# Object implementation
deviceServant = DeviceServant(1132, "master")
device = deviceServant._this() # How does this work? / Naming wrong

# FIXME: Move this somewhere else
print orb.object_to_string(device) # IOR

# Activating the POA
poa = orb.resolve_initial_references("RootPOA")
poa._get_the_POAManager().activate()

orb.run()

print "Server finished..."
