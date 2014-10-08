#!/usr/bin/python2.6
import gen_functions as gf
import sys
#from gen_functions import *
#Cfile = open ("other.txt","w")
#Assume a string is in binary unless the name ends in a 'H' meaning it's in hex
#See ###***### for a more fully commented section describing each step

#Don't care handeling
dcwH="FFFFFFFFFFFFFFF0"		#Don't care data word in hex, must match WORD in length
X=0							#Add in data memory used as a don't care in many instances, usually the last or 1st address, eg: 0 or 2047 

#Opcodes
nop	="000000"; add ="000001"; sub ="000010"; br ="011111"; eq ="001010"; lt = "001001";

#Initialisation
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]
r=0;s=0;t=0; #r = row number, s=strip number, t=tile number

######################################-TEST GENERATION-#######################################
#-----------------------------------------------------------------------------------------------------
#<<<<<<Test_branching: Uses rows 0-6 in strips 0_0 and 1_0, all other strips are loaded with TRUE_NOPS>>>>>
#-----------------------------------------------------------------------------------------------------
#Generate effectivly 2 while loops one after the other testing first branch if false (strip0) and second branch if true (strip1)

print "Generating branching tests"

#----Row0----------------------------------#
#--Strip0-----------------#
r=0;s=0;t=0;
opcode	= add
addr0	= gf.int_to_bin(0,gf.DADDR_BITS)
addr1	= gf.int_to_bin(2,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(0)

a_wordH = "000000000000000B" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1;
opcode	= eq
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(1,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(0,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.formatH_for_roach(dcwH)
a_wordH = "0000000000000001" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row1----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= br
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(1,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(1,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(0)

a_wordH = "0000000000000000" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= nop
addr0	= gf.int_to_bin(0,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(10)

a_wordH = "000000000000000A" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row2----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= add
addr0	= gf.int_to_bin(2,gf.DADDR_BITS)
addr1	= gf.int_to_bin(3,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(1)

a_wordH = "0000000000000005" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= add
addr0	= gf.int_to_bin(2,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(3)

a_wordH = "0000000000000005" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row3----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= lt
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(5,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(1,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(4)

a_wordH = "0000000000000000" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= add
addr0	= gf.int_to_bin(3,gf.DADDR_BITS)
addr1	= gf.int_to_bin(5,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(0)

a_wordH = "000000000000000B" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row4----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= nop
addr0	= gf.int_to_bin(3,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.formatH_for_roach(dcwH)

a_wordH = dcwH 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= br
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(0,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(0)

a_wordH = "0000000000000000" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row5----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= sub
addr0	= gf.int_to_bin(5,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(10)

a_wordH = "0000000000000004" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= add 
addr0	= gf.int_to_bin(5,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(1)

a_wordH = "0000000000000004" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----Row6----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= nop
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(6)

a_wordH = "0000000000000006" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= nop
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(3)

a_wordH = "0000000000000003" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1

#----All other strips, rows 0-6  -------------------#
#Fill all other strips with T_NOPS from rows 0 to 7	###****###
S_st = 2
S_end = gf.STRIPS-1 
R=0;s=0;t=0;
for t in range(0,gf.TILES):
		for s in range(S_st,S_end+1):
				for R in range(0,7):	#Write a row in a strip in a tile
						opcode	= nop
						addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
						addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
						addr2	= gf.int_to_bin(R,gf.DADDR_BITS)
						sel0	= gf.int_to_bin(s,3)	#set sel to the strip currently being written
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)	#Set the selq to the tile currently being written    
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
						i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
						i_wordH = gf.formatH_for_roach(i_wordH)	#Insert '\x' marks to indicate hex to python transmit script

						#Format final lines to be written to files
						word = i_word+":"+i_wordH				#Instruction line containing both the binary and roach formated instruction
						d_wordH = "Address %d:" %(R) + gf.formatH_for_roach(dcwH)	#Data word0 formatted for roach
						a_wordH = "Address %d:" %(R) + dcwH	#Answer word0 written in hex and indexed by row number, in this case a don't care

						#Write instruction and data words to file
						zI[t][s].write(word+"\n")
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")
		#After the 1st tile's remaining strips have been filled everyone else in the system gets T_NOPS for these rows
		S_st=0
print "Completed branching test: rows 0-6"
print "R = : ", R
print "r = : ", r


#----Row7----------------------------------#
#--Strip0-----------------#
s=0;
opcode	= nop
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(6)

a_wordH = "0000000000000006" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

#--Strip1-----------------#
s=1
opcode	= nop
addr0	= gf.int_to_bin(X,gf.DADDR_BITS)
addr1	= gf.int_to_bin(X,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

d_wordH = gf.roach_word(3)

a_wordH = "0000000000000003" 

#Format final lines to be written to files
word = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(word+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

r = r+1


gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1])
print "completed succesfully"
