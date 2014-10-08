#!/usr/bin/python2.6
# Client program
from socket import *
import os

# Create sending socket
s_host = "10.0.0.11"
s_port = 3157
s_addr = (s_host,s_port)

send_sock = socket(AF_INET,SOCK_DGRAM)
send_sock.connect(s_addr)

# Create receiving socket
r_host = "10.0.0.1"
r_port = 3158 
r_buf = 9000 #BYTES  
r_addr = (r_host,r_port)

receive_sock = socket(AF_INET,SOCK_DGRAM)
receive_sock.bind(r_addr)

data = range(0,64)
Pcount=0
done="\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x0c"
i=0

#Receives results directly
#Takes:
#Data: An array long enough to receive all packets coming back
#Pcount: A variable place holder containing zero
#done: a string containing the expected packet from hydra indicating the end of execution
def FastReceive(data,Pcount,done):
		while(1):
				data[Pcount],r_addr =receive_sock.recvfrom(r_buf)

				if data[Pcount]==done:
						break
		
				Pcount=Pcount+1

		results=[data,Pcount]
		return results


