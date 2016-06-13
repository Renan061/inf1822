#!/usr/bin/env python

import socket

# Setup
serverAddress = ("localhost", 1984)

# Socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(5)

print("New server on: " + str(serverAddress))

while True:
    # Accepts connections from outside
    (clientSocket, address) = serverSocket.accept()
    print("New connection with: " + str(address))

    # Does something with the clientSocket
    message = ""
    while True:
    	data = clientSocket.recv(4096)
    	if data:
    		message += data
    		print("Received: ", data)
    	else:
    		print("Stoped receiving...")
    		break
    print("Final message: " + message)

    clientSocket.close()