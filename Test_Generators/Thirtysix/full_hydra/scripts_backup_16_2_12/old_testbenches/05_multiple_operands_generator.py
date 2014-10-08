#!/usr/bin/python2.6
##Memory test: Load a unique value into every data location and increment by one.
import generator_functions as gf
import FP_creator as FP
import random

opcode_dict={0:"000000" , 1:"000001" , 2:"000010",3:"000011" , 4:"000101",5:"000110",6:"000111",7:"001100",8:"010100",9:"011100",10:"100100",11:"110100",12:"000010"}
opcode_names={0:"add" , 1:"sub", 2:"TRUE_NOP",3:"mul",4:"copy",5:"max",6:"min",7:"<",8:"==",9:"<=",10:">",11:">=",12:"HALF_NOP"}

#Initialisation
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]
r=0;s=0;t=0; #r = row number, s=strip number, t=tile number
print "Generating mem_test"

for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				d_wordH=range(gf.DROWS)	#initialise a new data word array
				a_wordH=range(gf.DROWS)	#initialise a new answer word array

				#Generate data, instructions and answers and write instructions to files
				for r in range(0,gf.IROWS):	#Write a row in a strip in a tile
						
						#Generate random values:
						var1I= random.randrange(-100,100)#var1= r
						var2I=random.randrange(-100,100)#var2= r+5
						
						var1FP=FP.custom_floating_point_creator (var1I,gf.D_wf,gf.D_we)
						var2FP=FP.custom_floating_point_creator (var2I,gf.D_wf,gf.D_we)
						
						var1H =gf.bin_to_hex_l(var1FP,64)
						var2H= gf.bin_to_hex_l(var2FP,64)
						
						d_wordH[r] = "Address %d:" %(r) + var1H
						d_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + var2H

						#Pick and preform operation
						op = random.randrange(0,12)
						opcode=opcode_dict[op]
						opname = opcode_names[op]

						if op== 0:#ADD
							answer = var1I+var2I
							answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
							answerH= gf.bin_to_hex_l(answerFP,64)
							#Writing the same answer to both operand addresses, this way reading from and writing to every address is tested
							a_wordH[r] = "Address %d:" %(r) + answerH
							a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH

						elif op== 1:#SUB
								answer = var1I-var2I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH

						elif op== 2:#TRUENOP
								a_wordH[r] = "Address %d:" %(r) + var1H
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + var2H
								answer = "NULL"

						elif op== 3:#MUL
								answer = var1I*var2I
								#Just put a note in the answers if it's going to be a negative zero
								sign=""
								if answer==0:
										if (var1I <0 and var2I>=0) or (var1I >=0 and var2I<0):
												sign = "neg"
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH+sign
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH+sign
						
						elif op== 4:#Copy
								answer = var1I
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
							
						elif op== 5:#MAX
								answer = max(var1I,var2I)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH

						elif op== 6:#MIN
								answer = min(var1I,var2I)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 7:# <
								if var1I<var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 8:# ==
								if var1I==var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 9:# <=
								if var1I<=var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 10:# >=
								if var1I>=var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 11:# >
								if var1I>var2I:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)

								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH[r] = "Address %d:" %(r) + answerH
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answerH
						
						elif op== 12:#HALF_NOP
								a_wordH[r] = "Address %d:" %(r) + var1H
								a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + "Unknown due to Half_nop"
								answer = "NULL"
						
						print "var1&2: ", var1I,var2I, "opcode: ", opcode_names[op], "Ans: ", answer


						#Generate instruction
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)			#Operand0
						addr1	= gf.int_to_bin(r+(gf.DROWS/2),gf.DADDR_BITS)		#Operand1

						if op == 2: #I'm implimenting OP==2 as a TRUE_NOP, op==12 is a HALF_NOP
								addr2	= gf.int_to_bin(r,gf.DADDR_BITS)		#Secondary address same as row so NOTHING will be written
						else:
								addr2	= gf.int_to_bin(r+(gf.DROWS/2),gf.DADDR_BITS)		#Secondary address

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
gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1])

print "completed succesfully"
