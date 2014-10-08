#!/usr/bin/python2.6
import generator_functions as gf
import FP_creator as FP
import sys
import random

####NOTES:
#System must contain at least the minimum of strips and tiles (3,2) and 8 data and instruction rows)
#Values higher than such will contain add operand where the same address is added to itself and stored in the same (implied) location

if gf.DROWS != gf.IROWS:
		print "ERROR: the number of data rows must be the same as the number of instruction rows for this script to be run"
		sys.exit()

print "Generating mem_test"

#Opcodes
nop	="000010"; add ="000000"; sub ="000001"; br ="001000"; eq ="010100"; lt = "001100"; cpy = "000101"; cpo="001001"; mul="000011";

#Initialisation
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]

######################################-TEST GENERATION-#######################################
#-----------------------------------------------------------------------------------------------------
#<<<<<<Test_branching: Uses rows 0-6 in strips 0_0 and 1_0, all other strips are loaded with TRUE_NOPS>>>>>
#-----------------------------------------------------------------------------------------------------
#Generate effectivly 2 while loops one after the other testing first branch if false (strip0) and second branch if true (strip1)

print "Generating branching tests"
r=0; s=0; t=0;
#----Row0----------------------------------#
#--Strip0-----------------#
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

varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (11,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#--Strip1-----------------#
s=1; 
opcode	= nop
addr0	= gf.int_to_bin(0,gf.DADDR_BITS)
addr1	= gf.int_to_bin(0,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#--Strip2-----------------#
s=2; 
opcode	= cpy #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(0,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (10,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#----Row1----------------------------------#
r=r+1;  
#--Strip0-----------------#
s=0
opcode	= lt 
addr0	= gf.int_to_bin(3,gf.DADDR_BITS)
addr1	= gf.int_to_bin(0,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP="1" #A logic answer not a floating point value
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip1-----------------#
s=1;
opcode	= nop
addr0	= gf.int_to_bin(1,gf.DADDR_BITS)
addr1	= gf.int_to_bin(1,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= cpo #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(0,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (10,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row2----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= br
addr0	= gf.int_to_bin(1,gf.DADDR_BITS)
addr1	= gf.int_to_bin(4,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (1,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip1-----------------#
s=1;
opcode	= nop
addr0	= gf.int_to_bin(2,gf.DADDR_BITS)
addr1	= gf.int_to_bin(2,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= nop #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row3----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= add
addr0	= gf.int_to_bin(3,gf.DADDR_BITS)
addr1	= gf.int_to_bin(0,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (10,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (21,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#--Strip1-----------------#
s=1;
opcode	= nop
addr0	= gf.int_to_bin(3,gf.DADDR_BITS)
addr1	= gf.int_to_bin(3,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= nop #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row4----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= nop
addr0	= gf.int_to_bin(4,gf.DADDR_BITS)
addr1	= gf.int_to_bin(4,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#--Strip1-----------------#
s=1;
opcode	= add 
addr0	= gf.int_to_bin(4,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (11,gf.D_wf,gf.D_we) #WHY not 12?
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= cpy #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(1,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (10,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row5----------------------------------#
r=r+1;
#--Strip0-----------------#
s=0
opcode	= nop 
addr0	= gf.int_to_bin(5,gf.DADDR_BITS)
addr1	= gf.int_to_bin(5,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (2,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (2,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)


#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#--Strip1-----------------#
s=1;
opcode	= lt 
addr0	= gf.int_to_bin(4,gf.DADDR_BITS)
addr1	= gf.int_to_bin(7,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP="0"
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= cpo #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(4,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (10,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row6----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= nop 
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (3,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (3,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)


#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#--Strip1-----------------#
s=1;
opcode	= br 
addr0	= gf.int_to_bin(5,gf.DADDR_BITS)
addr1	= gf.int_to_bin(8,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (1,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (1,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= nop #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row7----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= nop 
addr0	= gf.int_to_bin(7,gf.DADDR_BITS)
addr1	= gf.int_to_bin(7,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (4,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (4,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)


#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#--Strip1-----------------#
s=1;
opcode	= add 
addr0	= gf.int_to_bin(7,gf.DADDR_BITS)
addr1	= gf.int_to_bin(4,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (11,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (22,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= nop #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r

#----Row8----------------------------------#\
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= nop 
addr0	= gf.int_to_bin(8,gf.DADDR_BITS)
addr1	= gf.int_to_bin(8,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (5,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (5,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)


#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#--Strip1-----------------#
s=1;
opcode	= nop 
addr0	= gf.int_to_bin(8,gf.DADDR_BITS)
addr1	= gf.int_to_bin(8,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=FP.custom_floating_point_creator (4,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (4,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

print t,":",s,":",r
#--Strip2-----------------#
s=2; 
opcode	= nop #To save result from Strip0 for copying out next cycle
addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
sel0	= gf.int_to_bin(s,3)
sel1	= gf.int_to_bin(s,3)
selq	= gf.int_to_bin(t,3)

i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
i_wordH = gf.bin_to_hex(i_word) 
i_wordH = gf.formatH_for_roach(i_wordH)

varFP=random.randrange(0,100)
varFP=FP.custom_floating_point_creator (varFP,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
a_wordH = d_wordH

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
print t,":",s,":",r


###########Fill up the rest of the system ###############
#Fill out rest of the above strips if more rows than 8 with adds
print "Filling up the remaining rows in the 1st 3 strips of the 1st tile 9:end"
t=0
for s in range(0,3):
		for r in range(9,gf.DROWS):#DROWS==IROWS
				opcode	= add 
				addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
				sel0	= gf.int_to_bin(s,3)
				sel1	= gf.int_to_bin(s,3)
				selq	= gf.int_to_bin(t,3)
				
				i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
				i_wordH = gf.bin_to_hex(i_word) 
				i_wordH = gf.formatH_for_roach(i_wordH)
				
				varI=random.randrange(0,100)
				varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
				d_wordH = gf.bin_to_hex_l(varFP,64)
				ansFP =FP.custom_floating_point_creator ((varI+varI),gf.D_wf,gf.D_we)
				a_wordH = gf.bin_to_hex_l(ansFP,64)
				
				#Format final lines to be written to files
				i_wordH = i_word+":"+i_wordH	
				d_wordH = "Address %d:" %(r) + d_wordH
				a_wordH = "Address %d:" %(r) + a_wordH
				
				#Write instruction and data words to file
				zI[t][s].write(i_wordH+"\n")
				zD[t][s].write(d_wordH+"\n")
				zA[t][s].write(a_wordH+"\n")
				print t,":",s,":",r

#Fill out the 1st 9rows in any remaining strips in the 1st tile with nops (due to branching this is the easiest way of being sure of the final result in these rows)
print "Filling the 1st 9 rows of the remaining strips in the 1st tile 0:8"
t=0
for s in range(3,gf.STRIPS):
		for r in range(0,9):
				opcode	= nop
				addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
				sel0	= gf.int_to_bin(s,3)
				sel1	= gf.int_to_bin(s,3)
				selq	= gf.int_to_bin(t,3)
				
				i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
				i_wordH = gf.bin_to_hex(i_word) 
				i_wordH = gf.formatH_for_roach(i_wordH)
		
				varI= random.randrange(-100,100)
		
				varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
				d_wordH = gf.bin_to_hex_l(varFP,64)

				a_wordH = d_wordH

				#Format final lines to be written to files
				i_wordH = i_word+":"+i_wordH	
				d_wordH = "Address %d:" %(r) + d_wordH
				a_wordH = "Address %d:" %(r) + a_wordH

				#Write instruction and data words to file
				zI[t][s].write(i_wordH+"\n")
				zD[t][s].write(d_wordH+"\n")
				zA[t][s].write(a_wordH+"\n")
				print t,":",s,":",r

#Fill out the remaining rows in any remaining strips in the 1st tile with sub
print "Filling up remaining rows in remaining strips in 1st tile, 9:end"
t=0
for s in range(3,gf.STRIPS):
		for r in range(9,gf.DROWS):#DROWS==IROWS
				opcode	= sub #To save result from Strip0 for copying out next cycle
				addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
				addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
				sel0	= gf.int_to_bin(s,3)
				sel1	= gf.int_to_bin(s,3)
				selq	= gf.int_to_bin(t,3)
				
				i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
				i_wordH = gf.bin_to_hex(i_word) 
				i_wordH = gf.formatH_for_roach(i_wordH)
				
				varI=random.randrange(-100,100)
				varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
				d_wordH = gf.bin_to_hex_l(varFP,64)
#				ansFP =FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
				ansFP =FP.custom_floating_point_creator ((varI-varI),gf.D_wf,gf.D_we)
				a_wordH = gf.bin_to_hex_l(ansFP,64)
				
				#Format final lines to be written to files
				i_wordH = i_word+":"+i_wordH	
				d_wordH = "Address %d:" %(r) + d_wordH
				a_wordH = "Address %d:" %(r) + a_wordH
				
				#Write instruction and data words to file
				zI[t][s].write(i_wordH+"\n")
				zD[t][s].write(d_wordH+"\n")
				zA[t][s].write(a_wordH+"\n")
				print t,":",s,":",r

#Fill out all other tiles 
#First fill the 1st 9 rows in each strip with nops (due to branching this is the easiest way of being sure of the final result in these rows)
print "Filling up 1st 9 rows of remaining strips"
r=0; s=0; t=1;
for t in range(1,gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(0,9):
						opcode	= nop
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
						addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
						sel0	= gf.int_to_bin(s,3)
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
						i_wordH = gf.bin_to_hex(i_word) 
						i_wordH = gf.formatH_for_roach(i_wordH)
				
						varI= random.randrange(-100,100)
				
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						d_wordH = gf.bin_to_hex_l(varFP,64)
		
						a_wordH = d_wordH

						#Format final lines to be written to files
						i_wordH = i_word+":"+i_wordH	
						d_wordH = "Address %d:" %(r) + d_wordH
						a_wordH = "Address %d:" %(r) + a_wordH

						#Write instruction and data words to file
						zI[t][s].write(i_wordH+"\n")
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")
						print t,":",s,":",r
#Fill up the remaining rows in all these other strips with muls
print "Filling up remaining strips rows: 9:end"
r=9; s=0; t=1;
for t in range(1,gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(9,gf.DROWS):#DROWS==IROWS
						opcode	= mul 
						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)
						addr1	= gf.int_to_bin(r,gf.DADDR_BITS)
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)
						sel0	= gf.int_to_bin(s,3)
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
						i_wordH = gf.bin_to_hex(i_word) 
						i_wordH = gf.formatH_for_roach(i_wordH)
						
						varI=random.randrange(-100,100)
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						d_wordH = gf.bin_to_hex_l(varFP,64)
						#ansFP =FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						ansFP =FP.custom_floating_point_creator ((varI*varI),gf.D_wf,gf.D_we)
						a_wordH = gf.bin_to_hex_l(ansFP,64)
						
						#Format final lines to be written to files
						i_wordH = i_word+":"+i_wordH	
						d_wordH = "Address %d:" %(r) + d_wordH
						a_wordH = "Address %d:" %(r) + a_wordH
						
						#Write instruction and data words to file
						zI[t][s].write(i_wordH+"\n")
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")
						print t,":",s,":",r

gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1],a[2])
print "completed succesfully"
