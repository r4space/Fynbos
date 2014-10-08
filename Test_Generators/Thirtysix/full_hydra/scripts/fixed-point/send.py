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

#Read in all data to be sent
datIN=open("data.txt","r")
Darray=datIN.readlines()
datIN.close()



#Sending:
while (1):

		#If last packet is about to be sent
		if i==(len(Darray)-1):

				#Send a packet
				print("Sending last packet",i)
				send_sock.send(Darray[i])

				Results=FastReceive(data,Pcount,done)
				data=Results[0]
				Pcount=Results[1]
				print ("Finished receiving %d packets"%Pcount)
				break
		
		else:
				#Send a packet
				print("Sending packet",i)
				send_sock.send(Darray[i])
				i=i+1
		
				#Wait for a request for more data
				request,r_addr=receive_sock.recvfrom(r_buf)



#Close sockets
send_sock.close()
receive_sock.close()

#Post processing of data
g=0;
temp=range(8)
value=""
rf=open("Received_results","w")
print("Beginning post processing:")

for z in range(Pcount):
		for i in range(len(data[z])):
				temp[g] = hex(ord(data[z][i]))
				if len(temp[g])==4:
						temp[g] =temp[g][2:]
				else:
						temp[g] ='0'+temp[g][2:]
				g=g+1
				
				if (i+1)%8==0:
						for h in range(0,len(temp)):
								value=value+str(temp[h])
						
#						print value
						rf.write(value+"\n")
						g=0
						value = ""
rf.close()
print("Completed successfully, find results in \'Received_results\'")
