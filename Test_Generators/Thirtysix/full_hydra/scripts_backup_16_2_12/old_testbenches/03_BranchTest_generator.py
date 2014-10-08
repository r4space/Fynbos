#!/usr/bin/python2.6
import generator_functions as gf
import FP_creator as FP
import sys
import random

####NOTES:
## Assumes the following have been set in generator_functions.py:
##TILES = 2
##STRIPS = 3
##DROWS = 8
##IROWS = 8

#Opcodes
nop	="000010"; add ="000000"; sub ="000001"; br ="001000"; eq ="010100"; lt = "001100";

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

varFP=FP.custom_floating_point_creator (210,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)
ansFP=FP.custom_floating_point_creator (210,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

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

varFP=FP.custom_floating_point_creator (220,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (220,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

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

varFP=FP.custom_floating_point_creator (230,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (230,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

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

varFP=FP.custom_floating_point_creator (240,gf.D_wf,gf.D_we)
d_wordH = gf.bin_to_hex_l(varFP,64)

ansFP=FP.custom_floating_point_creator (240,gf.D_wf,gf.D_we)
a_wordH = gf.bin_to_hex_l(ansFP,64)

#Format final lines to be written to files
i_wordH = i_word+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")

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

#----Row6----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= nop 
addr0	= gf.int_to_bin(6,gf.DADDR_BITS)
addr1	= gf.int_to_bin(6,gf.DADDR_BITS)
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


#Rest of the system just adding itself to itself

#Last strip in tile0
s=2
for r in range(0,gf.IROWS):
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

		operand= random.randrange(-100,100)

		varFP=FP.custom_floating_point_creator (operand,gf.D_wf,gf.D_we)
		d_wordH = gf.bin_to_hex_l(varFP,64)

		ansFP=FP.custom_floating_point_creator (operand,gf.D_wf,gf.D_we)
		a_wordH = gf.bin_to_hex_l(ansFP,64)
	
		#Format final lines to be written to files
		i_wordH = i_word+":"+i_wordH	
		d_wordH = "Address %d:" %(r) + d_wordH
		a_wordH = "Address %d:" %(r) + a_wordH

		#Write instruction and data words to file
		zI[t][s].write(i_wordH+"\n")
		zD[t][s].write(d_wordH+"\n")
		zA[t][s].write(a_wordH+"\n")


#All other strips in all other tiles
r=0; s=0; t=1;
for t in range(1,gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(0,gf.IROWS):
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
				
						operand= random.randrange(-100,100)
				
						varFP=FP.custom_floating_point_creator (operand,gf.D_wf,gf.D_we)
						d_wordH = gf.bin_to_hex_l(varFP,64)
		
						ansFP=FP.custom_floating_point_creator (operand,gf.D_wf,gf.D_we)
						a_wordH = gf.bin_to_hex_l(ansFP,64)

						#Format final lines to be written to files
						i_wordH = i_word+":"+i_wordH	
						d_wordH = "Address %d:" %(r) + d_wordH
						a_wordH = "Address %d:" %(r) + a_wordH

						#Write instruction and data words to file
						zI[t][s].write(i_wordH+"\n")
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")

gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1],a[2])
print "completed succesfully"
