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
op = 0
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]
r=0;s=0;t=0; #r = row number, s=strip number, t=tile number
if gf.DROWS != gf.IROWS:
		print "ERROR: the number of data rows must be the same as the number of instruction rows for this script to be run"
		sys.exit()
print "Generating power_test"

#Generate random operand values:
var1I= random.randrange(-100,100)

instruction_count = 0
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				d_wordH=range(gf.DROWS)	#initialise a new data word array
				a_wordH=range(gf.DROWS)	#initialise a new answer word array

				#Generate data, instructions and answers and write instructions to files
				for r in range(0,gf.IROWS):	#Write a row in a strip in a tile

						instruction_count= instruction_count+1
						
						#Pick a operation --alternative between add and multiply
						if op == 3:
								op = 0
						else:
								op = 3
						
						opcode=opcode_dict[op]
						opname = opcode_names[op]

						#The same data address is used to provide both operands and the result is saved back into the same location
						var1FP=FP.custom_floating_point_creator (var1I,gf.D_wf,gf.D_we)
						var1H =gf.bin_to_hex_l(var1FP,64)
						d_wordH[r] = "Address %d:" %(r) + var1H

						if op== 0:#ADD
							answer = var1I+var1I
							answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
							answerH= gf.bin_to_hex_l(answerFP,64)
							#Writing the same answer to both operand addresses, this way reading from and writing to every address is tested
							a_wordH[r] = "Address %d:" %(r) + answerH

						elif op== 3:#MUL
								answer = var1I*var1I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
						
						print instruction_count,":  ", "var1: ", var1I, "opcode: ", opcode,":",opcode_names[op], "Ans: ", answer
						var1I=random.randrange(-100,100)

						#Generate instruction
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)		#Operand0
						addr1	= gf.int_to_bin(r,gf.DADDR_BITS)		#Operand1
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)		#Secondary address same as row so NOTHING will be written to the specified address, in the case of NOPs (2 or 12) NOTHING will be written

						sel0	= gf.int_to_bin(s,gf.STRIP_Ad_bits)	#set sel's to the strip currently being written
						sel1	= gf.int_to_bin(s,gf.STRIP_Ad_bits)
						selq	= gf.int_to_bin(t,gf.TILES_Ad_bits)	#Set the selq to the tile currently being written    
						
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
