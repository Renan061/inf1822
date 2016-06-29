
import sys

# ==================================================
#
#	Constants
#
# ==================================================

_CATALOGUE_MESSAGE_RECEIVER = "catalogue"
_CATALOGUE_MESSAGE_METHODS = ["register", "registerMaster", "deregister",
	"deregisterMaster", "getByType", "getMasterForType"]

# ==================================================
#
#	Catalogue
#
# ==================================================

# Used to parse a string message
def parse(string):
	# "receiver#method#args"
	pieces = string.split("#")

	# Receiver
	if len(pieces) != 3:
		_error("parsing message (len)")
	if pieces[0] != _CATALOGUE_MESSAGE_RECEIVER:
		_error("parsing message (receiver)")

	# Args
	args = pieces[2].split(",")

	# Method
	method = pieces[1]
	if method == _CATALOGUE_MESSAGE_METHODS[0]: # Register
		return Register(args)
	elif method == _CATALOGUE_MESSAGE_METHODS[1]: # registerMaster
		return RegisterMaster(args)
	elif method == _CATALOGUE_MESSAGE_METHODS[2]: # deregister
	    _error("deregisterMaster - not implemented for this test")
	elif method == _CATALOGUE_MESSAGE_METHODS[3]: # deregisterMaster
		_error("deregisterMaster - not implemented for this test")
	elif method == _CATALOGUE_MESSAGE_METHODS[4]: # getByType
		_error("getByType - not implemented for this test")
	elif method == _CATALOGUE_MESSAGE_METHODS[5]: # getMasterForType
		_error("getMasterForType - not implemented for this test")
	else:
		_error("parsing message (method)")

# Used to log errors and exit the program with an error
def _error(string):
	print("CatalogueMessage error - " + str(string))
	sys.exit()

# ==================================================
#
#	Messages
#
# ==================================================

# "catalogue#register#host(string),port(long),id(long),type(string),clusterId(long)"
class Register:
	def __init__(self, args):
		if len(args) != 5:
			_error("parsing message (len)")

		self.host = str(args[0])
		self.port = long(args[1])
		self.id = long(args[2])
		self.type = str(args[3])
		self.clusterId = long(args[4])

# "catalogue#registerMaster#host(string),port(long),id(long),type(string),clusterId(long)"
class RegisterMaster:
	def __init__(self, args):
		if len(args) != 5:
			_error("parsing message (len)")

		self.host = str(args[0])
		self.port = long(args[1])
		self.id = long(args[2])
		self.type = str(args[3])
		self.clusterId = long(args[4])

