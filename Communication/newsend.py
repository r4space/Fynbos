#!/usr/bin/python2.6

#SETUP:
DWORD_LENGTH = 64

# Client program
from socket import *
import os
import binascii
import time
import pylab as pl
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
setdefaulttimeout(2)

#data = range(0,9e6)
data = range(5000000)
Pcount=0
i=0
c=0
#Receives results directly
#Takes:
#Data: An array long enough to receive all packets coming back
#Pcount: A variable place holder containing zero
#done: a string containing the expected packet from hydra indicating the end of execution
#def FastReceive(data,Pcount,done,finish):
def FastReceive(data,Pcount):
		cpo_count=0
		count=0
		end_exec = []
		while(1):
				try:
						data[Pcount],r_addr =receive_sock.recvfrom(r_buf)
						cpo_count=cpo_count+1
						print "pcount: ", Pcount
				except error.message, msg:
						#except send_sock.error, msg:
						print "An error occured receiving the results", msg
				
				word=process_a_coms_message(data[Pcount])
				print "word: ", word



						
				if Pcount ==8:
						end_exec.append(time.time())
						print "TIME1: ",end_exec[0]
						break

#				elif Pcount == 20:
#						end_exec.append(time.time())
#						print "TIME2: ",end_exec[1]
#	  					break
#Uncomment this to find out how many packets to expect and adjust above number but using this for real data collection will mean lossing a portion of the 1st packet for some reason				
				if data[Pcount][-16:-8]=='\xbb\xbb\xee\xee\xaa\xaa\xdd\xdd'and count==0:
						end_exec.append(time.time())
						print "caught one at recieved packet: ", cpo_count
						cpo_count=0

						count = count+1
				elif data[Pcount][-16:-8]=='\xbb\xbb\xee\xee\xaa\xaa\xdd\xdd' and count==1:
							end_exec.append(time.time())
							print "end_Exec: ", end_exec
							print "I ended cause I found the end"
							print "cpo_count: ", cpo_count
							break
				
				Pcount=Pcount+1
				
		results=[data,Pcount,end_exec]
		return results

def process_a_coms_message (word):
		g=0
		temp=range(8)
		value=""
		returning=["nop","nop","nop","nop"]
		fred=0

#		for i in range(len(word)):
		for i in range(32):
				temp[g] = hex(ord(word[i]))
				if len(temp[g])==4:
						temp[g] =temp[g][2:]
				else:
						temp[g] ='0'+temp[g][2:]
				g=g+1
				
				if (i+1)%8==0:
						for h in range(0,len(temp)):
								value=value+str(temp[h])
						
								returnword=value[(16-DWORD_LENGTH/4):]
						g=0
						value = ""
#						print "Returnword: ", returnword
						returning[fred]=returnword
						fred=fred+1
#		print "returning: ", returning
		return returning

#def process_a_word (word):
#		g=0
#		temp=range(8)
#		value=""
#		for i in range(len(word)):
#				temp[g] = hex(ord(word[i]))
#				if len(temp[g])==4:
#						temp[g] =temp[g][2:]
#				else:
#						temp[g] ='0'+temp[g][2:]
#				g=g+1
#				
#				if (i+1)%8==0:
#						for h in range(0,len(temp)):
#								value=value+str(temp[h])
#						
#								returnword=value[(16-DWORD_LENGTH/4):]+"\n"
#						g=0
#						value = ""
#		return returnword

#Read in all data to be sent
datIN=open("./outgoing_data/data.txt","r")
Darray=datIN.readlines()
datIN.close()

for j in range(0,len(Darray)):
				Darray[j]=Darray[j].strip()

request = range(0,len(Darray)-1)



print "len darr: ", len(Darray)
#Sending:
for_div=0
accum=0
beginsending=time.time()
for i in range(len(Darray)):

		#If last packet is about to be sent
		if i==(len(Darray)-1):

				#Send a packet
				#print("Sending last packet",i)
				try:
						send_sock.send(binascii.unhexlify(Darray[i]))
				except error.message, msg:
						print "An error occured sending the last packet",msg

				start_execution = time.time()
				print "start; %e" %(start_execution)
				Results=FastReceive(data,Pcount)

				data=Results[0]
				Pcount=Results[1]
				end_execution = Results[2][0]
				print "end_execution: %e" %(end_execution)
				offload_finished = Results[2][1]
				print ("Finished receiving %d packets"%(Pcount+1))
				break
		
		#Make sending of 2nd last packet not wait for a reply from host as it won't get one(all data and instructions now loaded)
		elif i==(len(Darray)-2):

				#Send a packet
				#print("Sending 2nd last packet",i)
#				raw_input(">>?")
				try:
						send_sock.send(binascii.unhexlify(Darray[i]))
				except error.message, msg:
						#except send_sock.error, msg:
						print "An error occured sending the 2ndlast packet: ",msg
		else:
				#Send a packet
#				print("Sending packet",i)
				sendtime=time.time()
				try:
						send_sock.send(binascii.unhexlify(Darray[i]))
				except error.message, msg:
						#except send_sock.error, msg:
						print "An error occured sending the previous packet: ",msg
		
				#Wait for a request for more data
				while (1):
						try:
								request[i],r_addr=receive_sock.recvfrom(r_buf)
						except error.message, msg:
								print "An error occured receiving a request from hydra", msg
					
#						packet_words= process_a_coms_message(request[i])
#						print "Recieved communication: ", packet_words
#						if packet_words[2] == "000000000000000b" or packet_words[2] == "000000000000000a":
						if request[i][-16:-8]=='\x00\x00\x00\x00\x00\x00\x00\x0b' or request[i][-16:-8]=='\x00\x00\x00\x00\x00\x00\x00\x0a':
								#						print "recieved correct request: "
								endtime=time.time()
								break
				i=i+1
				accum = accum+(endtime-sendtime)
				for_div=for_div+1

#Close sockets
send_sock.close()
receive_sock.close()

print "average send and recieve next request time: %e" %(accum/for_div)
print "for div: ", for_div

#Post processing of data
g=0;
temp=range(8)
value=""
rf=open("./received_data/Received_results","w")
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
						
						rf.write(value[(16-DWORD_LENGTH/4):]+"\n")
						g=0
						value = ""
rf.close()
LOAD_TIME1=accum
LOAD_TIME2=start_execution-beginsending

EXEC_time=end_execution - start_execution

OFF_LOAD=offload_finished-end_execution

LOAD_TO_OFFLOAD=offload_finished-beginsending

print("Completed successfully, find results in \'Received_results\'")

print "Load time (time from start to last packet delivered: %e, %e" %(LOAD_TIME1,LOAD_TIME2)

print "Execute time:(time from last packet sent to last copy out packet received): %e" %(EXEC_time)

print "Time to off-load (last copy out arrived-last-offload arrived): %e" %(OFF_LOAD)

print "Total from 1st packet to initiate execution to last off load recieved: %e" %(LOAD_TO_OFFLOAD)

				






