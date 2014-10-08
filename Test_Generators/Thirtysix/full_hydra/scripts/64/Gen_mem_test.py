#!/usr/bin/python2.6
import generator_functions as gf
import FP_creator as FP
import sys
import random


#Initialisation
a =	gf.initialise_files(gf.STRIPS,gf.TILES)
zI =a[0] #Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA =a[2] #Array of handles on answer files: zA[tile][strip]

######################################-TEST GENERATION-#######################################
###########Fill up data system ###############
print "Generating data words for a %dx%d with %d words per strip: total number of data words being: "%(gf.STRIPS,gf.TILES,gf.DROWS),gf.DROWS*gf.STRIPS*gf.TILES
for t in range(0, gf.TILES):
		for s in range(0,gf.STRIPS):
				for r in range(0,gf.DROWS):
						varI=random.randrange(0,100000)
						varFP=FP.custom_floating_point_creator (varI,gf.D_wf,gf.D_we)
						d_wordH = gf.bin_to_hex_l(varFP,64)
						d_wordH = "Address %d:" %(r) + d_wordH
						zD[t][s].write(d_wordH+"\n")
						zA[t][s].write(d_wordH+"\n")
						
print "Generating nop instruction words for a %dx%d with %d instructions per strip: total number of instructions being: "%(gf.STRIPS,gf.TILES,gf.IROWS),gf.IROWS*gf.STRIPS*gf.TILES
nop = "000010"
for t in range(0, gf.TILES):
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
				
						i_wordH = "Address %d:" %(r)+i_wordH	
						zI[t][s].write(i_wordH+"\n")

print "Completed all generation succesfully"
