#!/usr/bin/env python

import socket

serverAddress = ('localhost', 1984)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(serverAddress)
clientSocket.send("catalogue#register#localhost,1900,1,client,1")
clientSocket.close()