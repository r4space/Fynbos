#!/usr/bin/python2.6
import generator_functions as gf
import shutil
import os
#This file compiles all the generated instruction and data files into a roach_transmission file which contains all data and instructions compiled into packets with their system commands for transmission to roach.  How the packets are structured is a further test,used to verify Hydra's communication system.
#NOTE: It is assumed that the program input here FILLS the system, i.e that something is written to every data and instruction location even if that is just zeros and it is therefore assumed that the inputs supply these zeros.  The implication is that no provision is made for checking if only half a strip is to be loaded and the construction of the additional system commands that would require.  This doesn't mean loading half a strip isn't tested only that in reading the input files checks are not done to see if a strip is only half filled

#TEST IMAGES:
#1) Operational image: This is a load image which would actually be used for operation, i.e as few packets are used as possible with only coincidental boundarytests 
#2) Communication test image: This is a load image where as many potential problem cases are created as possible including accessing both sides of memory, strip, tile and packet boundaries repeatedly.
ZERO_WORD_RH = "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"  #A zero filled roach formatted hexidecimal word
###########-Test LOAD_DATA-###############
#1)	Test a full load of the system in as few packets as necessary

###################################################################################
#Pack data into hydra system blocks inserting system commands
###################################################################################
cmd="010"
string=""
LDprogram=""
pcounter=0		#Packets needed counter, just for debugging and monitoring purposes
rcounter=0		#Lines read and written counter to enable packet counting, also just for debugging and monitoring purposes
count=0			#Word counter for command creation 

#Read out all data words from source hydra data files and concatinate them into a string
#Note this must be done rather than reading the data directly into a packet due to need to put the system command word ahead of it's data.  That command can only be generated when the number of data words is known which is only possible after reading through all the files
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):

				i=open("../outputs/data/Df_%d_%d" %(t,s),"r")
				
				l=i.readlines()

				for j in range(0,len(l)):
						if rcounter%1120==0:#1120==0:#1024==0:
								pcounter=pcounter+1
						rcounter=rcounter+1

						l[j] = l[j].split(":")[1]	#Extract the roach formatted data only
						string=string+l[j].strip()
						count=count+1
				i.close()

#Pack the system commands needed into the string of data words at the needed locations
#If the load data command cannot store the count value for lack of bit space, multiple load_data commands are needed, this section inserts them at the correct locations or skips to just adding 1 load instructions command at the front of the string
len_dchunk = pow(2,gf.SC_len-gf.DADDR_BITS-9)-1	#Eg: 65536 = 2^16, 16 counter bits available in the LOAD_DATA command
print ("len_dchunck: ", len_dchunk)
print ("count: ", count)
if count > len_dchunk:	#65536 = 2^16, 16 counter bits available in sthe LOAD_DATA command
		#For as many LD commands are needed to count each data word, insert the correct LD command and add to program string
		Nosys_commands = count/len_dchunk
		print("nosys_command1: ", Nosys_commands)
		if count%len_dchunk >0:
				Nosys_commands = Nosys_commands+1

		print("nosys_command2: ", Nosys_commands)
		for i in range (0,Nosys_commands):
				p=i*len_dchunk*32
				
				if count>len_dchunk:
						new_count = len_dchunk
						count = count-len_dchunk
				else:
						new_count = count
				#new_count = len(string[p:p+(len_dchunk*32)])
				print ("new_count1: ", new_count)
				new_count= gf.int_to_bin(new_count,(gf.SC_len-gf.DADDR_BITS-9))	#How many words to load
				print ("new_count2: ", new_count)

				start_add = gf.hydra_Daddr(i*len_dchunk)
				row= gf.int_to_bin(start_add[0],gf.DADDR_BITS)
				strip= gf.int_to_bin(start_add[1],3)
				tile= gf.int_to_bin(start_add[2],3)
				start=row+strip+tile

				command=new_count+start+cmd
				commandH = gf.bin_to_hex(command) 
				commandH = gf.formatH_for_roach(commandH)
				LDprogram=LDprogram+commandH+string[p:p+(len_dchunk*32)]+ZERO_WORD_RH+ZERO_WORD_RH



else:	#If it happens to fit within one packet executing this is shorter
		start= gf.int_to_bin(0,gf.DADDR_BITS+6)
		count= gf.int_to_bin(count,gf.SC_len-gf.DADDR_BITS-9)	#How many words to load
		command=count+start+cmd
		commandH = gf.bin_to_hex(command) 
		commandH = gf.formatH_for_roach(commandH)
		LDprogram=commandH+string+ZERO_WORD_RH+ZERO_WORD_RH
		Nosys_commands = 1

print("LD command1: ", command)
print("\nPacked data portion of the program with system commands, %d data words were read\n" %rcounter)
print("%d hydra system commands are needed to load this data\n" %Nosys_commands)
print("The length of the LDprogram is %d: " %len(LDprogram))
print("%d UDP packets are needed to transfer this data\n" %pcounter)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
###################################################################################


###################################################################################
#Pack instructions into hydra system blocks with system commands
###################################################################################
cmd="001"
string=""
LIprogram =""
pcounter=0		#Packets needed counter, just for debugging and monitoring purposes
rcounter=0		#Lines read and written counter to enable packet counting, also just for debugging and monitoring purposes
count=0 		#Word counter for command creation 

#Read out all instruction words from source hydra data files and concatinate them into a string
#Note this must be done rather than reading the instructions directly into a packet due to the need to put the system command word ahead of it's instructions.  That command can only be generated when the number of instructions is known which is only possible after reading through all the files...
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):

				i=open("../outputs/instructions/If_%d_%d" %(t,s),"r")
				
				l=i.readlines()
				
				for j in range(0,len(l)):
						if rcounter%1120==0:	#1024==0: #1120==0:
								pcounter=pcounter+1
						rcounter=rcounter+1
								
						l[j] = l[j].split(":")[1]	#Extract the roach formatted data only
						string=string+l[j].strip()
						count=count+1

				i.close()

#Pack the system commands needed into the string of instructions at the needed locations
#If the load instructions command cannot store the count value for lack of bit space, multiple load_data commands are needed, this section inserts them at the correct locations or skips to just adding 1 load instructions command at the front of the string

len_ichunk = pow(2,gf.SC_len-gf.IADDR_BITS-9)-1	#Eg: 65536 = 2^16, 16 counter bits available in the LOAD_DATA command
if count > len_ichunk:
		#For as many LI commands are needed to count each instruction word, insert the correct LI command and add to program string
		Nosys_commands = count/len_ichunk
		if count%len_ichunk >0:
				Nosys_commands = Nosys_commands+1
		for i in range (0,Nosys_commands):
				p=i*len_ichunk*32		

				if count>len_dchunk:
						new_count = len_dchunk
						count = count-len_dchunk
				else:
						new_count = count

				print ("new_count1: ", new_count)
				new_count= gf.int_to_bin(new_count,gf.SC_len-gf.IADDR_BITS-9)#How many words to load
				print ("new_count2: ", new_count)

				start_add = gf.hydra_Iaddr(i*len_ichunk)
				row= gf.int_to_bin(start_add[0],gf.IADDR_BITS)
				strip= gf.int_to_bin(start_add[1],3)
				tile= gf.int_to_bin(start_add[2],3)
				start=row+strip+tile

				command=new_count+start+cmd
				commandH = gf.bin_to_hex(command) 
				commandH = gf.formatH_for_roach(commandH)
				LIprogram=LIprogram+commandH+string[p:p+(len_ichunk*32)]+ZERO_WORD_RH+ZERO_WORD_RH

else:	#If it happens to fit within one packet executing the following is quicker
		start= gf.int_to_bin(0,gf.IADDR_BITS+6)
		count= gf.int_to_bin(count,gf.SC_len-gf.IADDR_BITS-9)	#How many words to load
		command=count+start+cmd
		commandH = gf.bin_to_hex(command) 
		commandH = gf.formatH_for_roach(commandH)
		LIprogram=commandH+string+ZERO_WORD_RH+ZERO_WORD_RH
		Nosys_commands = 1

print ("LI command1: ", command)
print("Packed instruction portion of the program with system commands, %d instruction words were read\n" %rcounter)
print("%d hydra system commands are needed to load these instructions\n" %Nosys_commands)
print("The length of the LIprogram is %d: " %len(LIprogram))
print("%d UDP packets are needed to transfer these instructions\n" %pcounter)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

###################################################################################
#Create run and ofld commands

#Run command
#FOr the purposes of testing execution starts at row 0 and end at the last row in the system by default
cmd="011"
start = gf.int_to_bin(0,gf.IADDR_BITS)			#Start at row zero by default	
end = gf.int_to_bin((gf.IROWS-1),gf.IADDR_BITS)	#End at the last row by default
command=end+start+cmd
commandH = gf.bin_to_hex(command) 
run_commandH = gf.formatH_for_roach(commandH)
print ("This is the run command: ", command)

#Off Load command
#For the purposes of testing EVERYTHING is offloaded from the data memory
cmd="100"
tile = gf.int_to_bin((gf.TILES-1),3)
strip = gf.int_to_bin((gf.STRIPS-1),3)
row = gf.int_to_bin((gf.DROWS-1),gf.DADDR_BITS)
start = row+strip+tile
end = gf.int_to_bin(0,gf.SC_len-gf.DADDR_BITS-9)	#Irrelavent, just filling with zero's
command=end+start+cmd		
commandH = gf.bin_to_hex(command) 
ofld_commandH = gf.formatH_for_roach(commandH)
print ("This is the OFLD command: ", command)

###################################################################################
#Put whole program into one string, packetize the string and write packets to sender script
###################################################################################
Program = LDprogram+LIprogram+run_commandH+ZERO_WORD_RH+ofld_commandH+ZERO_WORD_RH

#Write program to file as one packet per line
dataF = open("../outputs/data.txt","w")

#Write packets to file
pcounter2=0
packet=''
for i in range(0,len(Program),35840):	#35840=32*1120, 32=length in the program string of a 64bit roach word, 1120=packet size of 1121 64bit words-1 to insert a starting zero word
		packet=packet+Program[i:i+35840]
		dataF.write(packet+"\n")
		packet=''
		pcounter2=pcounter2+1
dataF.close()
print("Packed WHOLE program which fits into %d packets" %(pcounter2))

###################################################################################
#Pack answers into a single file and count how many packets should be expected
###################################################################################
pcounter=0		#Packets expected counter, just for debugging and monitoring purposes
rcounter=0		#Lines read and written counter to enable packet counting, also just for debugging and monitoring purposes
a=open("../outputs/answers_file","w")

#Read out all the answer words from source hydra data files and write them consequtively into one file for verification
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):

				i=open("../outputs/answers/Af_%d_%d" %(t,s),"r")
				
				l=i.readlines()

				for j in range(0,len(l)):
						if rcounter%1088==0:#1024==0:
								pcounter=pcounter+1
						rcounter=rcounter+1

						l[j] = l[j].split(":")[1]	#Extract the roach formatted data only
						word=l[j].strip()
						a.write(word+"\n")

				i.close()

a.close()

#	Test loading only 99% of a strip in a packet twice
 #	Test loading only one strip in a packet twice in a row
 #	Test loading 99% of a tile in a packet twice in a row
#	Test loading only one tile in a packet twice in a row
 #	Test loading 99% of the system


###########-Test LOAD_INSTRUCTIONS-###############

###########-Test OFF_LOADING-###############

###########-Test RUNNING-###############



