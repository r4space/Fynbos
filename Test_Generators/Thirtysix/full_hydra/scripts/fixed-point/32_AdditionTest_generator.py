#!/usr/bin/python2.6
##Memory test: Load a unique value into every data location and increment by one.
import generator_functions as gf
import random
#Assume a string is in binary unless the name ends in a 'H' meaning it's in hex
add ="000001";

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
						var1= random.randrange(0,17179869183)
						#var1= r
						var1H =gf.roach_word(var1)
						var2=random.randrange(0,17179869183)
						#var2= r+5
						var2H= gf.roach_word(var2)
						d_wordH[r] = "Address %d:" %(r) + var1H
						d_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + var2H
						
						#Generate answers
						answer = str(hex(var1+var2))
						answer = answer[2:]
						while len(answer) != 16:
								answer = '0'+answer
						a_wordH[r] = "Address %d:" %(r) + answer	
						a_wordH[r+(gf.DROWS/2)] = "Address %d:" %(r+(gf.DROWS/2)) + answer	#Writing the same answer to both operand addresses, this way reading from and writing to every address are tested

						#Generate instruction
						opcode	= add
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)			#Operand0
						addr1	= gf.int_to_bin(r+(gf.DROWS/2),gf.DADDR_BITS)		#Operand1
						addr2	= gf.int_to_bin(r+(gf.DROWS/2),gf.DADDR_BITS)		#Secondary address
						sel0	= gf.int_to_bin(s,3)	#set sel's to the strip currently being written
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)	#Set the selq to the tile currently being written    
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
						i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
						i_wordH = gf.formatH_for_roach(i_wordH)	#Insert '\x' marks to indicate hex to python transmit script

						#Format final lines to be written to files
						word = i_word+":"+i_wordH				#Instruction line containing both the binary and roach formated instruction

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
