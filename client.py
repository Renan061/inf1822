#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import INF1822, INF1822__POA

# 
# Client
# 

print "Client started..."

# ORB setup
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Object
ior = sys.argv[1]
obj = orb.string_to_object(ior)
device = obj._narrow(INF1822.Device)

if device is None:
	print "Object reference is not an Example::Echo"
else:
	print device.id
	print device.type

print "Client finished..."
