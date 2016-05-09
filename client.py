#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer
import CosNaming, INF1822

# 
# Client
# 

print "Client started..."

# ORB setup
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

# Obtain a reference to the root naming context
obj = orb.resolve_initial_references("NameService")
rootContext = obj._narrow(CosNaming.NamingContext)
if rootContext is None:
    print "Failed to narrow the root naming context"
    sys.exit(1)

# Resolve the name "server.inf1822/INF1822Device.Object"
name = [CosNaming.NameComponent("server", "inf1822"),
        CosNaming.NameComponent("INF1822Device", "Object")]
try:
    obj = rootContext.resolve(name)
except CosNaming.NamingContext.NotFound, ex:
    print "Name not found"
    sys.exit(1)

# Narrow the object to an INF1822::Device
device = obj._narrow(INF1822.Device)
if device is None:
    print "Object reference is not an INF1822::Device"
    sys.exit(1)

# Doing something
print device.id
print device.type

print "Client finished..."
