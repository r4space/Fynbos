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

import sys
import floatconversion
fc = floatconversion
<<<<<<< TREE
import intconversion as ic
#ic = intconversion
=======
import intconversion
ic = intconversion
>>>>>>> MERGE-SOURCE

###Parameters#################################################
DATA_SIZE_C = 36
REGS_Ad_bits = 11
TILES_Ad_bits = 3
STRIPS_Ad_bits = 3
INSTR_WIDTH_C = 48

###File_Initialisations############################################
outputFile1 = "Current_Instructions.txt"
outputFile2 = "Hydra_inputs.txt"
outputFile3 = "Instructions_in_45bit_format.txt"
outputFile4 = "formatted_for_ROACH.txt"

CI = open(outputFile1,"w") 
HI = open(outputFile2,"w")
I45 = open(outputFile3,"w")
FFR = open(outputFile4,"w")


###Initialisation_and_zero'ing#####################################
#Note: many of the values set here are done so for the purposes of testing Hydra only and not intended for use in actual programs
number = sys.argv[1] #number of statements to be taken in
int_or_real = sys.argv[2] #Are the statements to be entered going to be ints or reals, 0 = reals, 1 = ints
num = int(number)
int_real = int(int_or_real)

addr0 = range (0,REGS_Ad_bits)		#operand1
addr1 = range (0,REGS_Ad_bits)		#operand2
addr2 = range (0,REGS_Ad_bits)		#secondary result storage location
sel0 = range (0,STRIPS_Ad_bits)
sel1 = range (0,STRIPS_Ad_bits)
selq0 = range (0,TILES_Ad_bits)

for i in range (0,REGS_Ad_bits):
		addr0[i] = 0;	
		addr1[i] = 0;	
		addr2[i] = 0;	

addr1[REGS_Ad_bits-1] = 1 #second operand address is 1 address ahead of first operand (for testing sake only)
addr2[REGS_Ad_bits-1] = 1 #Making the address for MUX3 output to be stored at same as where operand 2 was stored (for testing sake only)

for i in range (0,STRIPS_Ad_bits):
		sel0[i] = 0;	#For testing only)
		sel1[i] = 0;	#For testing only)
#for i in range (0,p.TILES_Ad_bits):
		selq0 =[0,0,1];	#selcting the 1st input from another tile to be saved instead of the result again just to be different (for testing only)

data = [[0,0,0] for i in range (2*num)]		#Data array with the same data item stored in 3 formates: hex, decimal, binary
dss = ["" for i in range(2*num)]			#Data array
iss = ["" for i in range(num)]				#Instructions array
Ass = []									#Generic array
INSTR = range (0, num)						#Array of instructions in 
I45_list = []								#Array of instructions in 

#Create data and matching instructions
w=0
for j in range (0,2*num,2):
		tempinst = range (0, INSTR_WIDTH_C)
		type = int_real
#		type = input("Enter operand type (0 = real, 1 = integer): ")

		if type == 0: #REAL

				print "Operand 1:",
				data[j] = fc.myreal()
				print "Operand 2:",
				data[j+1] = fc.myreal()

				op = raw_input("Enter operator: ")
				#instruction 31-26
				if op == '+':
						tempinst[14:20] = [1,1,0,1,1,0]

				elif op == '-':
						tempinst[14:20] = [1,1,0,1,1,1]
				
				elif op == '*':
						tempinst[14:20] = [1,1,1,0,0,0]

				elif op == '/':
						tempinst[14:20] = [1,1,1,0,0,1]

				elif op == 'br':
						tempinst[14:20] = [0,1,1,1,1,1]

				elif op == 'cp':
						tempinst[14:20] = [1,1,1,0,1,0]

				elif op == 'max':
						tempinst[14:20] = [1,1,1,0,1,1]

				elif op == 'min':
						tempinst[14:20] = [1,1,1,1,0,0]

				elif op == '>':
						tempinst[14:20] = [1,1,1,1,0,1]
				
				elif op == '<':
						tempinst[14:20] = [1,1,1,1,1,0]

				elif op == '=':
						tempinst[14:20] = [1,1,1,1,1,1]
				
				elif op == 'nop':
						tempinst[14:20] = [0,0,0,0,0,0]


		elif type ==1:	#INTEGER

				print "Operand 1:",
				data[j] = ic.myint()
				print "Operand 2:",
				data[j+1] = ic.myint()
		
				op = raw_input("Enter operator: ")
				#instruction 31-26
				if op == '+':
						tempinst[14:20] = [0,0,0,0,0,1] 

				elif op == '-':
						tempinst[14:20] = [0,0,0,0,1,0]
				
				elif op == '*':
						tempinst[14:20] = [0,0,0,0,1,1]

				elif op == '/':
						tempinst[14:20] = [0,0,0,1,0,0]

				elif op == 'br':
						tempinst[14:20] = [0,1,1,1,1,1]

				elif op == 'cp':
						tempinst[14:20] = [0,0,0,1,0,1]

				elif op == 'max':
						tempinst[14:20] = [0,0,0,1,1,0]

				elif op == 'min':
						tempinst[14:20] = [0,0,0,1,1,1]

				elif op == '>':
						tempinst[14:20] = [0,0,1,0,0,0]
				
				elif op == '<':
						tempinst[14:20] = [0,0,1,0,0,1]

				elif op == '=':
						tempinst[14:20] = [0,0,1,0,1,0]

				elif op == 'nop':
						tempinst[14:20] = [0,0,0,0,0,0]

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
		tempinst[37:48] = addr0 
		#instruction 19-10
		tempinst[26:37] = addr1
		#instruction 22-20
		tempinst[23:26] = sel0
		#instruction 25-23
		tempinst[20:23] = sel1
		#instruction 34-32
		tempinst[11:14] = selq0
		#instruction 44-35
		tempinst[0:11] = addr2

		#store as 45bits in binary and hex
		I45_list.append([fc.printable_vec(tempinst),fc.printable_vec(fc.bin_to_hex(tempinst))])

		#Save in binary format for hydra input
		iss[w] =fc.printable_vec(tempinst)
		
		#Convert to hex for human readability
		tempinst = fc.bin_to_hex(tempinst)
		
		#Convert hex to printable string
		tempinst = fc.printable_vec(tempinst)

		INSTR[w] =tempinst
		w=w+1
		
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
		
###Create system commands####################################################
##LOAD INSTRUCTION COMMAND--
tile = (0,0,0) #0
strip = (0,0,0) #0
row = (0,0,0,0,0,0,0,0,0,0,0) #0
count = fc.Intdec_to_bin(num-1,17)
LI = range (0,36)
LI[33:36] = (0,0,1) #COMMAND type [2-0]
LI[16:33] = row+strip+tile #starting address [18-3]
LI[0:16] = count	#how many instructions to load[31-19]

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
row = (0,0,0,0,0,0,0,0,0,0,0) #0
count = fc.Intdec_to_bin(num*2,17)
LD = range (0,36)
LD[33:36] = (0,1,0) #COMMAND type [2-0]
LD[16:33] = row+strip+tile #starting address [18-3]
LD[0:16] = count	#how many data points to load[36-19]

#save in binary:
Ass.append(fc.printable_vec(LD))
	#Append data 
Ass = Ass+dss

C_LD = fc.bin_to_hex(LD)
CI.write("\nLOAD_DATA command: ")
CI.write(fc.printable_vec(C_LD))

## RUN COMMAND
start =[0,0,0,0,0,0,0,0,0,0,0]#0
stop = fc.Intdec_to_bin(num-1,REGS_Ad_bits)
<<<<<<< TREE
filler= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
=======
filler= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
>>>>>>> MERGE-SOURCE
R = range (0,36)
R[33:36] = [0,1,1] #COMMAND type [2-0]
R[27:33] = filler[0:6] #Filler filling up strip&tile addr spaces as irrelevant for starting execution address [8:3]
R[16:27] = start #starting "row/register" [18:9]
R[5:16] = stop #Stop "row/register" [28:19]
R[:5] = filler[:5] #unused[35-29]

#save in binary:
Ass.append(fc.printable_vec(R))

C_R = fc.bin_to_hex(R)
CI.write("\nRUN command: ")
CI.write(fc.printable_vec(C_R))

## OFF_LOAD COMMAND
tile = [0,0,0] #0
strip = [0,0,0] #0
row = fc.Intdec_to_bin(num-1,REGS_Ad_bits)
OL = range (0,36)
OL[33:36] = [1,0,0] #COMMAND type [2-0]
OL[16:33] = row+strip+tile # Address to start off loading from [19-3]
OL[:16] = filler[:16] #Irrelevant

#save in binary:
Ass.append(fc.printable_vec(OL))

C_OL = fc.bin_to_hex(OL)
CI.write("\nOFF_LOAD command: ")
CI.write(fc.printable_vec(C_OL))

###Print input in ROACH readable form###############################################
###Load instruction command
FFR.write("\nLOAD_INSTR command: \n"),
t=fc.printable_vec(C_LI)
print "Hello!:, this is t: ", t
print "Len t", len(t)
s=""
for y in range(1,len(t),2):
				print "Loop: ", y
				s=s+str("\\x"+t[y-1]+t[y])
print "s: ",s
s="\\x0"+str(t[0])+s
print "s2: ",s
f=str("\\x00\\x00"+s+"\n")
print "f:",f
FFR.write(f)

###Instructions array
FFR.write("\nInstruction array: \n"),
s=""
for z in range (0,len(INSTR)):
		for y in range(0,len(INSTR[z]),2):
						s=s+str("\\x"+INSTR[z][y]+INSTR[z][y+1])
		f=str("\\x00\\x00"+s+"\n")
		s=""
		FFR.write(f)

###Load data command
FFR.write("\nLOAD_DATA command: \n"),
t=fc.printable_vec(C_LD)
s=""
for y in range(1,len(t),2):
				s=s+str("\\x"+t[y-1]+t[y])
s="\\x0"+str(t[0])+s
f=str("\\x00\\x00"+s+"\n")
FFR.write(f)

###Data array
FFR.write("\nData array: \n"),
s=""
for z in range (0,len(data)):
		print "data[z[]0]:",data[z][0]
		print "str(data[z[]0]):",str(data[z][0])
		for y in range(1,len(data[z][0]),2):
						s=s+str("\\x"+str(data[z][0][y])+str(data[z][0][y+1]))
		s="\\x0"+str(t[0])+s
		f=str("\\x00\\x00\\x00"+s+"\n")
		print "s:",s
		print "f:",f
		s=""
		FFR.write(f)

###RUN command
FFR.write("\nRUN command: \n"),
t=fc.printable_vec(C_R)
s=""
for y in range(1,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
s="\\x0"+str(t[0])+s
f=str("\\x00\\x00\\x00"+s+"\n")
FFR.write(f)

###Off Load command
FFR.write("\nOFF_LOAD command: \n"),
t=fc.printable_vec(C_OL)
s=""
for y in range(1,len(t),2):
				s=s+str("\\x"+t[y]+t[y+1])
s="\\x0"+str(t[0])+s
f=str("\\x00\\x00\\x00"+s+"\n")
FFR.write(f)

###Print human readable list of execution statments##################################
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
