#!/usr/bin/python2.6
# Client program
import struct
from socket import *
import ctypes

# Set the socket parameters
host = "10.0.0.11"
port = 3157
buf = 1024
addr = (host,port)

# Create socket
sock = socket(AF_INET,SOCK_DGRAM)
sock.connect(addr)

#Packet assebler inserts the rest from here
