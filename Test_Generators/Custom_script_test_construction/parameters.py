#!/usr/bin/python2.6
#Storage file for all parameters used
#Width of data words (am planning on increasing this to 26bits in the very near future and it could possibly be another trade-off parameter)
#Number of tiles
#Number of strips
#Number of bits used to address the instruction and data memories
#Opcode width
#Number of bits used to address the strips's ID's themselves (same parameter applies to the MUX selectors)
#Number of bits used to address the tiles's ID's themselves (same parameter applies to the MUX selectors)
#Instruction word width
#Number of registers (execution lines)

#GENERAL
DATA_SIZE_C= 32
NO_TILES_C = 4	
NO_STRIPS_C = 4

#ADDRESSING
INSTRUCTION_ADDR_C = 11
OPCODE_C = 6	
STRIPS_Ad_bits = 3
TILES_Ad_bits = 3
REGS_Ad_bits = 10	
INS_ADDR_C = REGS_Ad_bits+STRIPS_Ad_bits+TILES_Ad_bits
PC_RANGE_C = 2**REGS_Ad_bits
INSTR_WIDTH_C = REGS_Ad_bits+REGS_Ad_bits+STRIPS_Ad_bits+STRIPS_Ad_bits+OPCODE_C+TILES_Ad_bits+REGS_Ad_bits
NO_REGS_C = 2**REGS_Ad_bits




#NUMERICS:
FIXED_HIGH = 17 #Number of bit in the data words designated to the whole number(integer) portion of the word.
FIXED_LOW = 15	#Number of bit in the data words designated to the fractional (decimal) number portion.

