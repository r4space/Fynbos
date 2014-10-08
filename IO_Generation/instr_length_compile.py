#!/usr/bin/python2.7
from math import log, ceil

tiles=8
strips=7
#divs=4
NO_dregs=1024
NO_iregs=1024

opcode=6

tileadbits=ceil(log(tiles,2))
stripadbits=ceil(log(strips,2))
dregad=ceil(log(NO_dregs,2))
iregad=ceil(log(NO_iregs,2))

ilength=dregad+tileadbits+opcode+stripadbits+stripadbits+dregad+dregad

INS_ADDR_CD = dregad+stripadbits+tileadbits
INS_ADDR_CI = iregad+stripadbits+tileadbits
INS_ADDR_C = max(INS_ADDR_CD,INS_ADDR_CI)

## Decimal integer to number of binary bits needed#############
#Takes in a signed integer and returns the number of bits needed to represent it in binary
def int_to_bin_length (int_in):
		a = []
		i=0
		k = abs(int_in)
		print "k: ", k
		while k != 0:
				a.append(k%2)
				k = k/2
		length=len(a)
		return length


#max_load_count = ceil(log((strips*tiles*max(NO_dregs, NO_iregs)),2))
#max_load_count_length = int_to_bin_length(strips*tiles*max(NO_dregs,NO_iregs))
max_load_count_length = int_to_bin_length(tiles*strips*max(NO_dregs,NO_iregs))
print "max_load_count_length:", max_load_count_length

SC_LEN=INS_ADDR_C+3+max_load_count_length  #LI and LD are the largest possible command instructions determined by the number of registers in either the d    ata or instruction memory, the length is therefore controled by the number of bits needed to control this which depends on memory depths and number of st    rips

print "STRIPS: ", strips
print "TILES: ", tiles
print "NO_DREGS: ", NO_dregs
print "NO_IREGS: ", NO_iregs
print "strip_add_bits: ", stripadbits
print "tile_add_bits: ", tileadbits
print "INS_ADDR_CD: ", INS_ADDR_CD
print "INS_ADDR_CI: ", INS_ADDR_CI
print "INS_ADDR_C: ", INS_ADDR_C
print "INSTR_WDITH_C: ", ilength
print "SC_LEN: ", SC_LEN
print "Dregaddress bits: ", dregad
print "Iregaddress bits: ", iregad

