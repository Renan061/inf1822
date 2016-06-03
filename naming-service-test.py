#!/usr/bin/env python

import sys
import aux
import NamingService, NamingService__POA

# ==================================================
#
#	Main
#
# ==================================================

print "Test started..."

# Starting
orbManager = aux.ORBManager()

# Getting the object manager
filename = sys.argv[1]
ior = aux.readIorFromFile(filename)
objectManager = orbManager.getObjectFrom(ior, NamingService.ObjectManager)
if objectManager is None:
	print("IOR Error...")
	sys.exit(1)

# Registering with the naming service
print(objectManager.register("ior", "name", "type"))

print "Test finished..."