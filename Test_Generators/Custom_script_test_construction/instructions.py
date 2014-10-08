#!/usr/bin/python2.6
#Generates instructions for hydra based on some preset parameters:
#The script takes in an argument when run, the integer number of how many operation staments you want
#Following this a series of questions require inputs, basically the statements need to be entered
#For the moment, the MUX selectors are stuck at value 0, uncommenting can make them increment with each consequtive operation entered
#similarily, the starting off load address is hardcoded in as from Tile0 Strip0 register 10
#Similarily, the offload, load and running starting and stopping positions are hard coded in as follows:
#	-Data and instructions are loaded from tile0:strip0:reg0
#	-Programs are run from address 0 for as many statements as were entered
#	-Offloading begins at register 10 of strip0:tile0
#The output writen to the file Current_instructions.txt which will contain a list of all operations enetered, the strip instructions for such and the HYDRA coimmands needed to LOAD and exucute the program
#The output file hydra_inputs.txt is the program that will be entered into Hydra itself written in text binary as a series of 32bit words

import parameters 
p = parameters
import sys
import floatconversion
fc = floatconversion
import integerconversion
ic = integerconversion

###break_instruction############################
#Break a 45 bit instruction into to consecutive 32bit words
def break_instr (instr):
		TwoWords = [3, 4]
		word1 = instr[0:p.DATA_SIZE_C]
		word2 = instr[32:45]+[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

		TwoWords[0] = word1
		TwoWords[1] = word2
		return TwoWords

#INSTRUCTIONS
number = sys.argv[1] #number of statements to be taken in
num = int(number)
outputFile1 = "Current_Instructions.txt"
outputFile2 = "Hydra_inputs.txt"
outputFile3 = "Instructions_in_45bit_format.txt"
outputFile4 = "formatted_for_ROACH.txt"

#outputFile1 = "tempCurrent_Instructions.txt"
#outputFile2 = "tempHydra_inputs.txt"
#outputFile3 = "tempInstructions_in_45bit_format.txt"

CI = open(outputFile1,"w")
HI = open(outputFile2,"w")
I45 = open(outputFile3,"w")
FFR = open(outputFile4,"w")


#Initialisation and zero'ing
addr0 = range (0,p.REGS_Ad_bits)
addr1 = range (0,p.REGS_Ad_bits)
addr2 = range (0,p.REGS_Ad_bits)
sel0 = range (0,p.STRIPS_Ad_bits)
sel1 = range (0,p.STRIPS_Ad_bits)
selq0 = range (0,p.TILES_Ad_bits)

for i in range (0,p.REGS_Ad_bits):
		addr0[i] = 0;
		addr1[i] = 0;
		addr2[i] = 0;
addr1[9] = 1 #second operand address is 1 address ahead of first operand
addr2[9] = 1 #Making the adress for MUX3 output to be stored at same as where operand 2 was stored

for i in range (0,p.STRIPS_Ad_bits):
		sel0[i] = 0;
		sel1[i] = 0;
#for i in range (0,p.TILES_Ad_bits):
		selq0 =[0,0,1];	#selcting the 1st input from another tile to be saved instead of the result again just to be different


data = [[0,0,0] for i in range (2*num)]
dss = ["" for i in range(2*num)]
iss = ["" for i in range(2*num)]
Ass = []
INSTR = range (0, 2*num)
I45_list = []

#Create data and matching instructions
for j in range (0,2*num,2):
		tempinst = range (0, 45)
		type = input("Enter operand type (0 = real, 1 = integer): ")

		if type == 0: #REAL

				print "Operand 1:",
				data[j] = fc.myreal()
				print "Operand 2:",
				data[j+1] = fc.myreal()

				op = raw_input("Enter operator: ")
				#instruction 31-26
				if op == '+':
						tempinst[13:19] = [1,1,0,1,1,0]

				elif op == '-':
						tempinst[13:19] = [1,1,0,1,1,1]
				
				elif op == '*':
						tempinst[13:19] = [1,1,1,0,0,0]

				elif op == '/':
						tempinst[13:19] = [1,1,1,0,0,1]

				elif op == 'br':
						tempinst[13:19] = [0,1,1,1,1,1]

				elif op == 'cp':
						tempinst[13:19] = [1,1,1,0,1,0]

				elif op == 'max':
						tempinst[13:19] = [1,1,1,0,1,1]

				elif op == 'min':
						tempinst[13:19] = [1,1,1,1,0,0]

				elif op == '>':
						tempinst[13:19] = [1,1,1,1,0,1]
				
				elif op == '<':
						tempinst[13:19] = [1,1,1,1,1,0]

				elif op == '=':
						tempinst[13:19] = [1,1,1,1,1,1]
				
				elif op == 'nop':
						tempinst[13:19] = [0,0,0,0,0,0]


		elif type ==1:	#INTEGER

				print "Operand 1:",
				data[j] = ic.myint()
				print "Operand 2:",
				data[j+1] = ic.myint()
		
				op = raw_input("Enter operator: ")
				#instruction 31-26
				if op == '+':
						tempinst[13:19] = [0,0,0,0,0,1] 

				elif op == '-':
						tempinst[13:19] = [0,0,0,0,1,0]
				
				elif op == '*':
						tempinst[13:19] = [0,0,0,0,1,1]

				elif op == '/':
						tempinst[13:19] = [0,0,0,1,0,0]

				elif op == 'br':
						tempinst[13:19] = [0,1,1,1,1,1]

				elif op == 'cp':
						tempinst[13:19] = [0,0,0,1,0,1]

				elif op == 'max':
						tempinst[13:19] = [0,0,0,1,1,0]

				elif op == 'min':
						tempinst[13:19] = [0,0,0,1,1,1]

				elif op == '>':
						tempinst[13:19] = [0,0,1,0,0,0]
				
				elif op == '<':
						tempinst[13:19] = [0,0,1,0,0,1]

				elif op == '=':
						tempinst[13:19] = [0,0,1,0,1,0]

				elif op == 'nop':
						tempinst[13:19] = [0,0,0,0,0,0]

		#store operation
		s = str(data[j][1])+" "+op+" "+data[j+1][1]+"\n"
		CI.write(s)

		dss[j] = ""
		for i in range(0,len(data[j][2])):
				dss[j] = dss[j]+str(data[j][2][i])
#		HI.write(dss1+"\n")

		dss[j+1] = ""
		for i in range(0,len(data[j+1][2])):
				dss[j+1] = dss[j+1]+str(data[j+1][2][i])
#		HI.write(ss2+"\n")

		#instruction 9-0
		tempinst[35:45] = addr0 
		#instruction 19-10
		tempinst[25:35] = addr1
		#instruction 22-20
		tempinst[22:25] = sel0
		#instruction 25-23
		tempinst[19:22] = sel1
		#instruction 34-32
		tempinst[10:13] = selq0
		#instruction 44-35
		tempinst[0:10] = addr2

		#store as 45bits in binary and hex
		I45_list.append([fc.printable_vec(tempinst),fc.printable_vec(fc.bin_to_hex(tempinst))])

		#Split it into 2 32bit words
		tempinst = break_instr(tempinst)
		
		#Save in binary format for hydra input
		iss[j] =fc.printable_vec(tempinst[0])
		iss[j+1] =fc.printable_vec(tempinst[1])
		
		#Convert to hex for human readability
		tempinst[0] = fc.bin_to_hex(tempinst[0])
		tempinst[1] = fc.bin_to_hex(tempinst[1])
		#Convert hex to printable string
		tempinst[0] = fc.printable_vec(tempinst[0])
		tempinst[1] = fc.printable_vec(tempinst[1])

		INSTR[j] =tempinst[0]
		INSTR[j+1] =tempinst[1]
		
		#increment address's by 2 (to get next TWO adresses!
		addr0 = fc.bin_add_one (addr0)
		addr0 = fc.bin_add_one (addr0)
		addr1 = fc.bin_add_one (addr1)
		addr1 = fc.bin_add_one (addr1)
		addr2 = fc.bin_add_one (addr2)
		addr2 = fc.bin_add_one (addr2)

		#for the fun of it, make the sel operators, increment too
	#	sel0 = fc.bin_add_one (sel0)
	#	sel1 = fc.bin_add_one (sel1)
	#	selq0 = fc.bin_add_one (selq0)
		
#COMMANDS:
##LOAD INSTRUCTION COMMAND
tile = (0,0,0) #0
strip = (0,0,0) #0
row = (0,0,0,0,0,0,0,0,0,0) #0
count = fc.Intdec_to_bin(num,13)
LI = range (0,32)
LI[29:32] = (0,0,1) #COMMAND type [2-0]
LI[13:29] = row+strip+tile #starting address [18-3]
LI[0:13] = count	#how many instructions to load[31-19]

#save in binary:
Ass.append(fc.printable_vec(LI))
#Append instructions
Ass = Ass+iss

#Format for Current_instructions
C_LI =fc.bin_to_hex(LI)
CI.write("\nLOAD_instruction command: ")
CI.write(fc.printable_vec(C_LI))


##LOAD DATA COMMAND
tile = (0,0,0) #0
strip = (0,0,0) #0
row = (0,0,0,0,0,0,0,0,0,0) #0
count = fc.Intdec_to_bin(num*2,13)
LD = range (0,32)
LD[29:32] = (0,1,0) #COMMAND type [2-0]
LD[13:29] = row+strip+tile #starting address [18-3]
LD[0:13] = count	#how many data points to load[31-19]

#save in binary:
Ass.append(fc.printable_vec(LD))
	#Append data 
Ass = Ass+dss

C_LD = fc.bin_to_hex(LD)
CI.write("\nLOAD_DATA command: ")
CI.write(fc.printable_vec(C_LD))

## RUN COMMAND
start =[0,0,0,0,0,0,0,0,0,0]#0
stop = fc.Intdec_to_bin(num-1,10)
filler= [0,0,0,0,0,0,0,0,0,0,0]
R = range (0,32)
R[29:32] = [0,1,1] #COMMAND type [2-0]
R[23:29] = filler[0:6] #
R[13:23] = start #starting
R[3:13] = stop
R[:3] = filler[:3] #unused[31-20]

#save in binary:
Ass.append(fc.printable_vec(R))

C_R = fc.bin_to_hex(R)
CI.write("\nRUN command: ")
CI.write(fc.printable_vec(C_R))

## OFF_LOAD COMMAND
tile = [0,0,0] #0
strip = [0,0,0] #0
row = fc.Intdec_to_bin(num,10)
OL = range (0,32)
OL[29:32] = [1,0,0] #COMMAND type [2-0]
OL[13:29] = row+strip+tile # Address to start off loading from [19-3]
OL[:13] = filler[:13] #Irelevant

#save in binary:
Ass.append(fc.printable_vec(OL))

C_OL = fc.bin_to_hex(OL)
CI.write("\nOFF_LOAD command: ")
CI.write(fc.printable_vec(C_OL))
##################TESTING#################
FFR.write("\nLOAD_INSTR command: ")
t=fc.printable_vec(C_LI)
print "LI: ",t
s=""
for y in range(0,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
f=str("\\x00\\x00\\x00\\x00"+s+"\n")
FFR.write(f)

FFR.write("\nInstruction array: ")
s=""
for z in range (0,len(INSTR)):
		for y in range(0,len(INSTR[z]),2):
						s=s+str("\\x"+INSTR[z][y]+INSTR[z][y+1])

		print "\\x00\\x00\\x00\\x00"+s
		
		f=str("\\x00\\x00\\x00\\x00"+s+"\n")
		s=""
		print str(INSTR[z])+"\n"
		FFR.write(f)



FFR.write("\nLOAD_DATA command: ")
t=fc.printable_vec(C_LD)
print "LD: ",t
s=""
for y in range(0,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
f=str("\\x00\\x00\\x00\\x00"+s+"\n")
FFR.write(f)

FFR.write("\nData array: ")
s=""
for z in range (0,len(INSTR)):
		for y in range(0,len(INSTR[z]),2):
						s=s+str("\\x"+INSTR[z][y]+INSTR[z][y+1])
		f=str("\\x00\\x00\\x00\\x00"+s+"\n")
		s=""
		FFR.write(f)



FFR.write("\nRUN command: ")
t=fc.printable_vec(C_R)
print "R: ",t
s=""
for y in range(0,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
f=str("\\x00\\x00\\x00\\x00"+s+"\n")
FFR.write(f)





FFR.write("\nOFF_LOAD command: ")
t=fc.printable_vec(C_OL)
print "OL: ",t
s=""
for y in range(0,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
f=str("\\x00\\x00\\x00\\x00"+s+"\n")
FFR.write(f)

##########################################


CI.write("\nInstruction array: ")
for j in range(0,len(INSTR)):
	CI.write(str(INSTR[j])+", ")

CI.write("\nData array: ")
for i in range(0,len(data)):
	CI.write(str(data[i][0])+", ")

for k in range(0,len(Ass)):
		HI.write(str(Ass[k])+"\n")

for u in range(0,len(I45_list)):
		I45.write(str(I45_list[u])+"\n")

CI.close()
HI.close()
I45.close()
