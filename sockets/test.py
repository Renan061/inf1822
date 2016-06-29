#!/usr/bin/env python

import sys, socket


if len(sys.argv) != 3:
	print "First parameter must be server host and second parameter must be server port..."
	sys.exit(1)
serverAddress = (str(sys.argv[1]), long(sys.argv[2]))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(serverAddress)
clientSocket.send("catalogue#registerMaster#localhost,1900,0,master,1")
clientSocket.close()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(serverAddress)
clientSocket.send("catalogue#register#localhost,1900,1,client,1")
clientSocket.close()