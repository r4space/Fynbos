#!/usr/bin/python2.6
import generator_functions as gf
import FP_creator as FP
import sys
import random
####NOTES:
#Rows 0<->3: Test branch when false
#Rows 4<->8: Test branch when true
#Rows 0<->5: Test copying out of data
#Rows 9<->X : Test inter-strip communication, X = 9+number of rows needed for inter-strip test (dep on No strips)
#Rows X+1<->Y: Test inter-tile communication, Y = X+1+number of rows needed for inter-tiles test (dep on No tiles)
#Rows Y+1<->Z: Test all strips simultaneously carrying out each operation once, Z = Y+1+number of opcodes to test, 11 currently
#Rest of the system filled with nops as instructions and random values for data
#Embedded in the above are also tests:
	#Test of writing to specfied addreses and implied addresses only when appropriate
#After all of the above has been finished the rest of the system is filled with nop up to the maximum instruction row and all remaining data rows are filled with random values

#Initialisation
cp = "000101"
cpo = "001001"
nop = "000010"
add="000000"
sub="000001"
mul="000011"
Max="000110"
Min="000111"
div="000100"
GT="100100"
GTE="110100"
LT="001100"
LTE="011100"
NE="101100"
EQ="010100"
BR="001000"

a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]
r=0;s=0;t=0; #r = row number, s=strip number, t=tile number

min_rows=gf.STRIPS+gf.TILES+21
if gf.DROWS < min_rows or gf.IROWS < min_rows:
		print "More data and intruction rows than you've given are needed for this test, The minimum number of each needed is:", min_rows
		print "Exiting now"
		sys.exit()

print "Generating branching tests"
#Rows 0-3: Test branching when false: 
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#--Strip2-----------------#
s=2; 
opcode	= cp #To save result from Strip0 for copying out next cycle
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#----Row1----------------------------------#
r=r+1;  
#--Strip0-----------------#
s=0
opcode	= LT 
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#----Row2----------------------------------#
r=r+1; 
#--Strip0-----------------#
s=0
opcode	= BR
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#--Strip2-----------------#
s=2; 
opcode	= cp #To save result from Strip0 for copying out next cycle
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#--Strip1-----------------#
s=1;
opcode	= LT 
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#--Strip1-----------------#
s=1;
opcode	= BR 
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

#----Row8----------------------------------#
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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r

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
i_wordH = str(r)+":"+i_wordH	
d_wordH = "Address %d:" %(r) + d_wordH
a_wordH = "Address %d:" %(r) + a_wordH

#Write instruction and data words to file
zI[t][s].write(i_wordH+"\n")
zD[t][s].write(d_wordH+"\n")
zA[t][s].write(a_wordH+"\n")
#print t,":",s,":",r


#Fill out the 1st 9rows in any remaining strips in the 1st tile with nops (due to branching this is the easiest way of being sure of the final result in these rows)
print ">>>R:",r
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
				i_wordH = str(r)+":"+i_wordH	
				d_wordH = "Address %d:" %(r) + d_wordH
				a_wordH = "Address %d:" %(r) + a_wordH

				#Write instruction and data words to file
				zI[t][s].write(i_wordH+"\n")
				zD[t][s].write(d_wordH+"\n")
				zA[t][s].write(a_wordH+"\n")
				#print t,":",s,":",r

#Fill out all other tiles 
#First fill the 1st 9 rows in each strip with nops (due to branching this is the easiest way of being sure of the final result in these rows)
print ">>>R:",r
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
						i_wordH = str(r)+":"+i_wordH	
						d_wordH = "Address %d:" %(r) + d_wordH
						a_wordH = "Address %d:" %(r) + a_wordH

						#Write instruction and data words to file
						zI[t][s].write(i_wordH+"\n")
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")
						#print t,":",s,":",r

#Inter-strip comms test
print ">>>R:",r
print "Generating inter-strip communication test"
cr =9 
NO_inter_strip=gf.STRIPS-1	#Number of instruction rows needed to test inter-strip communication
opcode=cp
for t in range(0,gf.TILES):
		for r in range(cr,cr+NO_inter_strip):	

				#Create operands and write them to data files
				operands = range(gf.STRIPS)
				for s in range(0,gf.STRIPS):
						
						varI= random.randrange(-100,100)
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						varH =gf.bin_to_hex_l(varFP,64)
						operands[s]=varH

						d_wordH = "Address %d:" %(r) + operands[s]
						zD[t][s].write(d_wordH+"\n")


				#Write answers to file
				#Shift operands along the correct number of times to put the answers into the correct strips
				for i in range(r+1):
						operands=[operands[-1]]+operands[:-1]	

				for s in range(0,gf.STRIPS):

						a_wordH = "Address %d:" %(r) + operands[s]
						zA[t][s].write(a_wordH+"\n")
						

				#Create and write instructions to file
				#Shift sel0_range along the correct number of times to select correct strips' operand to copy
				sel0_range=range(gf.STRIPS)
				for i in range(r+1):
						sel0_range=[sel0_range[-1]]+sel0_range[:-1]

				for s in range(0,gf.STRIPS):

						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand0
						addr1	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand1 (Is unused and meaningless for a copy
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)				#Specified address
						sel0	= gf.int_to_bin(sel0_range[s],3)				#Set to prearranged other strip
						sel1	= gf.int_to_bin(s,3)	#Operand1 set to local (it's meaningless)
						selq	= gf.int_to_bin(t,3)	#Set the selq to the tile currently being written    
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
						i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
						i_wordH = gf.formatH_for_roach(i_wordH)	#Insert buffer zeros
						i_wordH = "Address %d:" %(r) + i_wordH 
						zI[t][s].write(i_wordH+"\n")
						
##Create a single row nop accross the whole system to give the data memory offset needed to save the inter-tile copied data
cr= cr+NO_inter_strip
opcode=nop
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				r=cr
				#Zero written to the data rows
				varFP=FP.custom_floating_point_creator (0,gf.D_wf,gf.D_we)
				varH =gf.bin_to_hex_l(varFP,64)
				d_wordH = "Address %d:" %(r) + varH
				zD[t][s].write(d_wordH+"\n")

				#No answer written as the inter-tile test is going to write to this location

				#NOP instruction created and written
				addr0	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand0 (Meaningless for this operantion)
				addr1	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand1 (Meaningless for this operantion)
				addr2	= gf.int_to_bin(r,gf.DADDR_BITS)				#Specified address set to implied - TRUE_NOP
				sel0	= gf.int_to_bin(s,3)	#Set to local strip
				sel1	= gf.int_to_bin(s,3)	#Operand1 set to local (it's meaningless)
				selq	= gf.int_to_bin(t,3)	#Set to local tile    
				
				i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
				i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
				i_wordH = gf.formatH_for_roach(i_wordH)	#Insert buffer zeros
				i_wordH = "Address %d:" %(r) + i_wordH 
				zI[t][s].write(i_wordH+"\n")

##Inter-tile comms test
print ">>>R:",r
print "Generating inter-tile communication test"
NO_inter_tile=gf.TILES-1	#Number of instruction rows needed to test inter-tile communication
opcode=cp
cr=r+1
for s in range(0,gf.STRIPS):
		d_wordH_arr = range(gf.TILES)

		for r in range(cr,cr+NO_inter_tile):
				#Create operands and write them to data files
				operands = range(gf.TILES)
				for t in range(0,gf.TILES):
						varI= random.randrange(-100,100)
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						varH =gf.bin_to_hex_l(varFP,64)
						operands[t]=varH

						d_wordH = "Address %d:" %(r) + operands[t]
						zD[t][s].write(d_wordH+"\n")

						#D_wordH_arr is only used after all tiles are done, 
						# it's just easiest to create everytime and overwrite it than specify it only be made on the last run
						d_wordH_arr[t]=operands[t] 

				#Write answers to file for the 1row back (the current implied row will get overwritten next by the next row execution except for the last row in which case see ***
				#Shift operands along the correct number of times to put the answers into the correct strips
				for i in range(r-cr+1):
						#for i in range((r-(NO_inter_strip+1))+1):
						operands=[operands[-1]]+operands[:-1]	

				for t in range(0,gf.TILES):
						a_wordH = "Address %d:" %(r-1)+ operands[t]
						zA[t][s].write(a_wordH+"\n")
						
				#Create and write instructions to file
				#Shift sel0_range along the correct number of times to select correct strips' operand to copy
				selq_range=range(gf.TILES)
				for i in range(r-cr+1):
				#for i in range((r-(NO_inter_strip+1))+1):
						selq_range=[selq_range[-1]]+selq_range[:-1]

				for t in range(0,gf.TILES):

						addr0	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand0 
						addr1	= gf.int_to_bin(r,gf.DADDR_BITS)				#Operand1 
						addr2	= gf.int_to_bin(r-1,gf.DADDR_BITS)				#Set to 
						sel0	= gf.int_to_bin(s,3)	#Set to local strip
						sel1	= gf.int_to_bin(s,3)	#Operand1 set to local (it's meaningless)
						selq	= gf.int_to_bin(selq_range[t],3)	#Set the selq to pre shifted     
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	#Complete instruction in binary
						i_wordH = gf.bin_to_hex(i_word) #Complete instruction in hex 
						i_wordH = gf.formatH_for_roach(i_wordH)	#Insert buffer zeros
						i_wordH = "Address %d:" %(r) + i_wordH 
						zI[t][s].write(i_wordH+"\n")
		#***Write the last answer in as untouched/not overwritten(the same value that was loaded in for copying to another tile) due to all copied values being written into one row back - i.e the last row used for this test doesn't have it's data over written cause the test only overwrites data 1 row back so the values that a
		for t in range(0,gf.TILES):
						a_wordH = "Address %d:" %(cr+NO_inter_tile-1)+d_wordH_arr[t] 
						zA[t][s].write(a_wordH+"\n")
print ">>>R:",r
#Peak operation ops test
print "Generating every-operation-simultaneously test"
cr= cr+NO_inter_tile
print "CR: ",cr
opcode_arr = [add,sub,mul,Max,Min,GT,LT,GTE,LTE,NE,EQ]
for t in range(0, gf.TILES):
		for s in range(0, gf.STRIPS):
				index=0
				var1I= random.randrange(-100,100)
				print "rangeL ", range(cr,cr+11)
				for r in range(cr,cr+11):

						print "t:s:r:", t,s,r
						opcode=opcode_arr[index]

						#Create data and answers	
						NxtI = random.randrange(-100,100)

						var1FP=FP.custom_floating_point_creator (var1I,gf.D_wf,gf.D_we)
						var1H =gf.bin_to_hex_l(var1FP,64)
						d_wordH = "Address %d:" %(r) + var1H
						zD[t][s].write(d_wordH+"\n")

						#Different opcode cases		
						if opcode == add:
							answer = var1I+NxtI
							answerFP = FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
							answerH = gf.bin_to_hex_l(answerFP,64)
							a_wordH = "Address %d:" %(r) + answerH
		
						elif opcode == sub:
								answer = var1I-NxtI
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH = "Address %d:" %(r) + answerH
					
						elif opcode == mul:
								answer = var1I*NxtI
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH = "address %d:" %(r) + answerH
						
						elif opcode == Max:
								answer = max(var1I,NxtI)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH = "address %d:" %(r) + answerH
						
						elif opcode == Min:
								answer = min(var1I,NxtI)
								answerFP=FP.custom_floating_point_creator (answer,gf.D_wf,gf.D_we)
								answerH= gf.bin_to_hex_l(answerFP,64)
								a_wordH = "address %d:" %(r) + answerH
						
						elif opcode == GT:
								if var1I>NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
		
						elif opcode == LT:
								if var1I<NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
		
						elif opcode == GTE:
								if var1I>=NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
		
						elif opcode == LTE:
								if var1I<=NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
		
						elif opcode == NE:
								if var1I!=NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
						
						elif opcode == EQ:
								if var1I==NxtI:
										answer=gf.int_to_bin(1,gf.D_len)
								else:
										answer=gf.int_to_bin(0,gf.D_len)
								answerH= gf.bin_to_hex_l(answer,64)
								a_wordH = "address %d:" %(r) + answerH
		
						zA[t][s].write(a_wordH+"\n")
						var1I = NxtI
						
						#Create instructions
						addr0 = gf.int_to_bin(r,gf.DADDR_BITS)	#Operand0
						addr1 = gf.int_to_bin((r+1),gf.DADDR_BITS)#Operand1
						addr2	= gf.int_to_bin(r,gf.DADDR_BITS)#Specified address same as current row, only implied written to 
						sel0	= gf.int_to_bin(s,3)	#set sel's to the current strip
						sel1	= gf.int_to_bin(s,3)
						selq	= gf.int_to_bin(t,3)	#Set the selq to the current tile    
						
						i_word = addr2+selq+opcode+sel1+sel0+addr1+addr0	
						i_wordH = gf.bin_to_hex(i_word) 
						i_wordH = gf.formatH_for_roach(i_wordH)
						word = str(r)+":"+i_wordH
						zI[t][s].write(word+"\n")
		
						index=index+1 #Next operand

				#Write final "Nxt! word to row above this one and insert a nop instruction there too
				r=r+1
				Nxt1FP=FP.custom_floating_point_creator (NxtI,gf.D_wf,gf.D_we)
				Nxt1H =gf.bin_to_hex_l(Nxt1FP,64)
				d_wordH = "Address %d:" %(r) + Nxt1H 
				zD[t][s].write(d_wordH+"\n")
				a_wordH=d_wordH
				zA[t][s].write(a_wordH+"\n")
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
				word = str(r)+":"+i_wordH
				zI[t][s].write(word+"\n")
#
#Fill the rest of the system with nops
print ">>>R:",r
print "Filling the rest of the system with random values and TRUE_NOPS"
cr=r+1
#Create instructions
boo=0
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(cr,gf.IROWS):
						
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
						
						#Format final lines to be written to files
						#i_wordH = str(boo)+":"+i_wordH
						i_wordH = str(r)+":"+i_wordH
						boo=boo+1
						#Write instruction and data words to file
						zI[t][s].write(i_wordH+"\n")

#Create data
for t in range(0,gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(cr,gf.DROWS):
				
						print "t:s:r:", t,s,r
						varI= random.randrange(-100,100)
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						d_wordH = gf.bin_to_hex_l(varFP,64)

						#Format final lines to be written to files
						d_wordH = "Address %d:" %(r) + d_wordH
						a_wordH = d_wordH

						#Write instruction and data words to file
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(a_wordH+"\n")


#Close files
gf.close_files(gf.STRIPS,gf.TILES,a[0],a[1],a[2])
print "completed succesfully"
