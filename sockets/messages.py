
import sys

# ==================================================
#
#	Constants
#
# ==================================================

_CATALOGUE_MESSAGE_RECEIVER = "catalogue"
_CATALOGUE_MESSAGE_METHODS = ["register", "deregister"]

# ==================================================
#
#	Catalogue
#
# ==================================================

# "receiver#method#args"
# "catalogue#register#host(string),port(long),id(long),type(string),clusterId(long)"

class CatalogueMessage:
	# This should be __init__
	def _parse(self, string):
		pieces = string.split("#")
		if len(pieces) != 3:
			self._error("parsing message (len)")
		if pieces[0] != _CATALOGUE_MESSAGE_RECEIVER:
			self._error("parsing message (receiver)")
		self._method = pieces[1]
		if self._method not in _CATALOGUE_MESSAGE_METHODS:
			self._error("parsing message (method)")
		self._args = pieces[2].split(",")

	def _error(self, string):
		print("CatalogueMessage error - " + str(string))
		sys.exit()

class CatalogueRegisterMessage(CatalogueMessage):
	def __init__(self, string):
		self._parse(string)
		if len(self._args) != 5:
			self._error("parsing message (len)")

		self.host = str(self._args[0])
		self.port = long(self._args[1])
		self.id = long(self._args[2])
		self.type = str(self._args[3])
		self.clusterId = long(self._args[4])
