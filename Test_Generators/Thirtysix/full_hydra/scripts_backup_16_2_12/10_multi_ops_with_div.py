#!/usr/bin/python2.6
##Writing to the specified address is NOT tested here due to the number of data rows vs instruction rows
##For the same reason operand0 is taken from the same row as the instruction and the result written back there.  operand1 comes from the next row on and therefore the value used as operand1 in an instruction will be the value used as operand0 in the following instruction
##Also for the same reason only TRUE_NOPs are executed here, although the opcode dictionary contains a half nop it is treated as a true nop
import generator_functions as gf
import FP_creator as FP
import random
import sys

opcode_dict={0:"000000" , 1:"000001" , 2:"000010",3:"000011" , 4:"000101",5:"000110",6:"000111",7:"001100",8:"010100",9:"011100",10:"100100",11:"110100",12:"000010",13:"000100"}
opcode_names={0:"add" , 1:"sub", 2:"TRUE_NOP",3:"mul",4:"copy",5:"max",6:"min",7:"<",8:"==",9:"<=",10:">",11:">=",12:"HALF_NOP",13:"DIV"}

#Initialisation
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]
r=0;s=0;t=0; #r = row number, s=strip number, t=tile number
if gf.DROWS != gf.IROWS:
		print "ERROR: the number of data rows must be the same as the number of instruction rows for this script to be run"
		sys.exit()
print "Generating mem_test"

#Generate 2 starting random values:
var1I= random.randrange(-100,100)
var2I=random.randrange(-100,100)

#Create an array that indicates if a strip is capable of division or not
local_div_strips = gf.div_strips
div_strips_array = range(0,gf.TILES)
for i in range (0,gf.TILES):
		div_strips_array[i]=range(0,gf.STRIPS)

for i in range (gf.TILES-1, -1, -1):
		for k in range (gf.STRIPS-1, -1, -1):
				if local_div_strips == 0:
						div_strips_array[i][k] = 0
				else:
						div_strips_array[i][k] = 1
						local_div_strips=local_div_strips-1
print "div array:", div_strips_array

instruction_count = 0
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				d_wordH=range(gf.DROWS)	#initialise a new data word array
				a_wordH=range(gf.DROWS)	#initialise a new answer word array

				#Generate data, instructions and answers and write instructions to files
				for r in range(0,gf.IROWS):	#Write a row in a strip in a tile

						r2=r+1
						instruction_count= instruction_count+1
						#To handle the boundary case where the Irow is the last row in memory and therefore there isn't a second operand address bove it
						if r2 == gf.IROWS:
								r2=r
								var2I=var1I
						
						#Pick a operation
						#Pick an operation, division is limited to certain strips only
						if div_strips_array[t][s]==1: #If in the div_strips range let it possibly select div too
								#op = random.randrange(0,14)
							op = random.randrange(10,14)
						else:
							op = random.randrange(0,13)	#Range excluding division for the rest of the strips
						
						opcode=opcode_dict[op]
						opname = opcode_names[op]
						

						#Check for div by zero and re-generate a new number if the case
						while (var2I==0 and op == 13):
								var2I=random.randrange(-100,100)
						
						var1FP=FP.custom_floating_point_creator (var1I,gf.D_wf,gf.D_we)
						var2FP=FP.custom_floating_point_creator (var2I,gf.D_wf,gf.D_we)
						
						var1H =gf.bin_to_hex_l(var1FP,64)
						var2H= gf.bin_to_hex_l(var2FP,64)
						
						d_wordH[r] = "Address %d:" %(r) + var1H
						d_wordH[r2] = "Address %d:" %(r2) + var2H

						if op== 0:#ADD
							answer = var1I+var2I
							answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
							answerH= gf.bin_to_hex_l(answerFP,64)
							#Writing the same answer to both operand addresses, this way reading from and writing to every address is tested
							a_wordH[r] = "Address %d:" %(r) + answerH

						elif op== 1:#SUB
								answer = var1I-var2I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH

						elif op== 2:#TRUENOP
								a_wordH[r] = "Address %d:" %(r) + var1H
								answer = "NULL"

						elif op== 3:#MUL
								answer = var1I*var2I
								#Just put a note in the answers if it's going to be a negative zero
#								sign=""
								if answer==0: #To get the sign of zero correct
										if (var1I <0 and var2I>=0) or (var1I >=0 and var2I<0):
												answer = -0.0
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 4:#Copy
								answer = var1I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
							
						elif op== 5:#MAX
								answer = max(var1I,var2I)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH

						elif op== 6:#MIN
								answer = min(var1I,var2I)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 7:# <
								if var1I<var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 8:# ==
								if var1I==var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 9:# <=
								if var1I<=var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 10:# >
								if var1I>var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 11:# >=
								if var1I>=var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						elif op== 12:#HALF_NOP
								a_wordH[r] = "Address %d:" %(r) + var1H
								answer = "NULL"

						elif op==13:#DIV
								answer = float(var1I)/var2I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH

						
						print instruction_count,":  ", "var1&2: ", var1I,var2I, "opcode: ", opcode,":",opcode_names[op], "Ans: ", answer
						var1I=var2I
						var2I=random.randrange(-100,100)

						#Generate instruction
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)			#Operand0
						addr1	= gf.int_to_bin(r2,gf.DADDR_BITS)		#Operand1
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)		#Secondary address same as row so NOTHING will be written to the specified address, in the case of NOPs (2 or 12) NOTHING will be written

						sel0	= gf.int_to_bin(s,3)	#set sel's to the strip currently being written
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)	#Set the selq to the tile currently being written    
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
						i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
						i_wordH = gf.formatH_for_roach(i_wordH)	#Insert '\x' marks to indicate hex to python transmit script

						#Format final lines to be written to files
						word = opcode_names[op]+i_word+":"+i_wordH				#Instruction line containing both the binary and roach formatted instruction

						#Write instruction and data words to file
						zI[t][s].write(word+"\n")

				#Write data and answer arrays to files
				#This is done seperatly in order to write all the values sequentially despite them being generated out of order (one in the lower half of memory and one in the upper half for each instruction row)
				for i in range(0,gf.DROWS):
						zD[t][s].write(d_wordH[i]+"\n")
						zA[t][s].write(a_wordH[i]+"\n")
#Close files
gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1],a[2])

print "completed succesfully"
