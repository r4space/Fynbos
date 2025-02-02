#!/usr/bin/python2.6
import generator_functions as gf
import shutil
import os
#This file compiles all the generated instruction and data files into a roach_transmission file which contains all data and instructions compiled into packets with their system commands for transmission to roach.  How the packets are structured is a further test,used to verify Hydra's communication system.
#NOTE: It is assumed that the program input here FILLS the system, i.e that something is written to every data and instruction location even if that is just zeros and it is therefore assumed that the inputs supply these zeros.  The implication is that no provision is made for checking if only half a strip is to be loaded and the construction of the additional system commands that would require.  This doesn't mean loading half a strip isn't tested only that in reading the input files checks are not done to see if a strip is only half filled

#TEST IMAGES:
#1) Operational image: This is a load image which would actually be used for operation, i.e as few packets are used as possible with only coincidental boundarytests 
#2) Communication test image: This is a load image where as many potential problem cases are created as possible including accessing both sides of memory, strip, tile and packet boundaries repeatedly.
ZERO_WORD_RH = "0000000000000000"  #A zero filled roach formatted hexidecimal word
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
#	Note this must be done rather than reading the data directly into a packet due to need to put the system command word ahead of it's data.  
#	That command can only be generated when the number of data words is known which is only possible after reading through all the files
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

				#		if count > 600:
								#								print "HERE: ", t, ":", s, "count: ", count

				i.close()

#----------------------------------------------------------------------------------
#Pack the system commands needed into the string of data words at the needed locations
#	If the load data command cannot store the count value for lack of bit space, multiple load_data commands are needed, this section inserts them 
#	at the correct locations or skips to just adding 1 load instructions command at the front of the string
len_dchunk = pow(2,gf.SC_len-gf.DADDR_BITS-9)-1	#Eg: 65536 = 2^16, 16 counter bits available in the LOAD_DATA command
if count > len_dchunk:	#65536 = 2^16, 16 counter bits available in the LOAD_DATA command
		#For as many LD commands are needed to count each data word, insert the correct LD command and add to program string
		Nosys_commands = count/len_dchunk
		if count%len_dchunk >0:
				Nosys_commands = Nosys_commands+1

		for i in range (0,Nosys_commands):
				p=i*len_dchunk*16
				
				if count>len_dchunk:
						new_count = len_dchunk
						count = count-len_dchunk
				else:
						new_count = count

				new_count= gf.int_to_bin(new_count,(gf.SC_len-gf.DADDR_BITS-9))	#How many words to load

				start_add = gf.hydra_Daddr(i*len_dchunk)
				row= gf.int_to_bin(start_add[0],gf.DADDR_BITS)
				strip= gf.int_to_bin(start_add[1],3)
				tile= gf.int_to_bin(start_add[2],3)
				start=row+strip+tile

				command=new_count+start+cmd
				commandH = gf.bin_to_hex(command) 
				commandH = gf.formatH_for_roach(commandH)
				LDprogram=ZERO_WORD_RH+LDprogram+commandH+string[p:p+(len_dchunk*16)]+ZERO_WORD_RH



else:	#If it happens to fit within one packet executing this is shorter
		start= gf.int_to_bin(0,gf.DADDR_BITS+6)
		count= gf.int_to_bin(count,gf.SC_len-gf.DADDR_BITS-9)	#How many words to load
		command=count+start+cmd
		commandH = gf.bin_to_hex(command) 
		LD_commandH = gf.formatH_for_roach(commandH)
		LDprogram=ZERO_WORD_RH+LD_commandH+string+ZERO_WORD_RH
		Nosys_commands = 1

print "<<<<< LDcommand: ", commandH, " >>>>>"
print("\nPacked data portion of the program with system commands, %d data words were read\n" %rcounter)
print("%d hydra system commands are needed to load this data\n" %Nosys_commands)
print("The length of the LDprogram is %d: " %len(LDprogram))
print("%d UDP packets are needed to transfer this data" %pcounter)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#----------------------------------------------------------------------------------
#Pack instructions into hydra system blocks with system commands, the same restrictions apply as for data packing
cmd="001"
string=""
LIprogram =""
pcounter=0		#Packets needed counter, just for debugging and monitoring purposes
rcounter=0		#Lines read and written counter to enable packet counting, also just for debugging and monitoring purposes
count=0 		#Word counter for command creation 

#Read out all instruction words from source hydra data files and concatinate them into a string
#	Note this must be done rather than reading the instructions directly into a packet due to the need to put the system command word ahead of 
#	it's instructions.  That command can only be generated when the number of instructions is known which is only possible after reading through 
#	all the files...
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
print " ****************COUNT1: ", count

#Pack the system commands needed into the string of instructions at the needed locations
#	If the load instructions command cannot store the count value for lack of bit space, multiple load_data commands are needed, 
#	this section inserts them at the correct locations or skips to just adding 1 load instructions command at the front of the string

len_ichunk = pow(2,gf.SC_len-gf.IADDR_BITS-9)-1	#Eg: 65536 = 2^16, 16 counter bits available in the LOAD_INSTR command
if count > len_ichunk:
		#For as many LI commands are needed to count each instruction word, insert the correct LI command and add to program string
		Nosys_commands = count/len_ichunk
		if count%len_ichunk >0:
				Nosys_commands = Nosys_commands+1
		for i in range (0,Nosys_commands):
				p=i*len_ichunk*16		

				if count>len_dchunk:
						new_count = len_dchunk
						count = count-len_dchunk
				else:
						new_count = count

				new_count= gf.int_to_bin(new_count,gf.SC_len-gf.IADDR_BITS-9)#How many words to load

				start_add = gf.hydra_Iaddr(i*len_ichunk)
				row= gf.int_to_bin(start_add[0],gf.IADDR_BITS)
				strip= gf.int_to_bin(start_add[1],3)
				tile= gf.int_to_bin(start_add[2],3)
				start=row+strip+tile

				command=new_count+start+cmd
				commandH = gf.bin_to_hex(command) 
				commandH = gf.formatH_for_roach(commandH)
				LIprogram=ZERO_WORD_RH+LIprogram+commandH+string[p:p+(len_ichunk*16)]+ZERO_WORD_RH

else:	#If it happens to fit within one packet executing the following is quicker
		start= gf.int_to_bin(0,gf.IADDR_BITS+6) #address = IADDR_BITS+3bits for strip+3bits for tile
		count= gf.int_to_bin(count,gf.SC_len-gf.IADDR_BITS-9)	#How many words to load: goes into as many bits are left after the start address and the 3bits for setting the commadn type(LI in this case) hence 9

		print " ****************START: ", start
		print " ****************COUNT2: ", count
		command=count+start+cmd
		commandH = gf.bin_to_hex(command) 
		LI_commandH = gf.formatH_for_roach(commandH)
		LIprogram=ZERO_WORD_RH + LI_commandH+string+ZERO_WORD_RH
		Nosys_commands = 1

print "<<<<< LIcommand: ", commandH, " >>>>>"
print("Packed instruction portion of the program with system commands, %d instruction words were read\n" %rcounter)
print("%d hydra system commands are needed to load these instructions\n" %Nosys_commands)
print("The length of the LIprogram is %d: " %len(LIprogram))
print("%d UDP packets are needed to transfer these instructions" %pcounter)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#----------------------------------------------------------------------------------
#Create Run command
#	or the purposes of testing execution starts at row 0 and end at the last row in the system by default
cmd="011"
start = gf.int_to_bin(0,gf.IADDR_BITS)			#Start at row zero by default	
end = gf.int_to_bin((gf.IROWS-1),gf.IADDR_BITS)	#End at the last row by default
command=end+start+cmd
commandH = gf.bin_to_hex(command) 
RUN_commandH = gf.formatH_for_roach(commandH)
print "<<<<< RUNcommand: ", commandH, " >>>>>"

#----------------------------------------------------------------------------------
#Create off Load command
#	For the purposes of testing EVERYTHING is offloaded from the data memory
#	For now the number of data registers to be considered in each strip is assumed to be the same as the number of execution rows, 
#	this obviously does not have to be the case, a parameter just needs to be added to the xml
cmd="100"
tile = gf.int_to_bin((gf.TILES-1),3)
strip = gf.int_to_bin((gf.STRIPS-1),3)
row = gf.int_to_bin((gf.DROWS-1),gf.DADDR_BITS)
#row = gf.int_to_bin(2047,gf.DADDR_BITS)
start = row+strip+tile
numregs = gf.int_to_bin(gf.DROWS,gf.SC_len-gf.DADDR_BITS-9)
print "NUMREGS: ", numregs
command=numregs+start+cmd		
commandH = gf.bin_to_hex(command) 
OFLD_commandH = gf.formatH_for_roach(commandH)
print "<<<<< OFLDcommand: ", commandH, " >>>>>"

#----------------------------------------------------------------------------------
#Put the whole program into one string, packetize the string and write packets to sender script

Program = LDprogram + LIprogram + ZERO_WORD_RH + RUN_commandH + ZERO_WORD_RH + OFLD_commandH + ZERO_WORD_RH
print "LD", LD_commandH
print "LI: ", LI_commandH 
print "Run: ", RUN_commandH
print "OFLD: ", OFLD_commandH

#Write program to file as one packet per line
#	Note: 17920=16*1120, 16=length in the program string of a 64bit roach word, 1120=packet size of 1121 64bit words-1 to insert a starting zero word
dataF = open("../outputs/data.txt","w")
pcounter2=0
packet=''

for i in range(0,len(Program),17920):	
		packet=packet+Program[i:i+17920]

		#Gaurentee last packet is at least 3 words long
		while len(packet)<48:
				packet = packet+ZERO_WORD_RH

		dataF.write(packet+"\n")
		packet=''
		pcounter2=pcounter2+1

dataF.close()
print("Packed WHOLE program, which fits into %d packets, into; %s") %(pcounter2,'data.txt')

#Write simulation inputs to file:
simF = open("../outputs/sim.txt","w")
for i in range(0,len(Program),16):	#16=length of a 64bit roach word
		line1="sim_rx_data <= X\""+Program[i:i+16]+"\";"
		if i ==0:
				print line1
		line2="wait until sim_rx_ack = '1' and rising_edge(clk);"
		simF.write(line1+"\n")
		simF.write(line2+"\n")
simF.close()
print("Packed WHOLE program into a simulation inputs file; sim.txt")




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



