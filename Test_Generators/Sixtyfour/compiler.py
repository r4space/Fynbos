#!/usr/bin/python2.6
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node
import generator_functions as gf	#Note this generator_function is different to the one used in creating the test benches
import FP_creator as FP
#### #Pre-Notes:

#No answer file is generated for this script

#The xml is interpretted with the following equivalences made.  The RHS is the interpretation and the LHS the xml parameter:
	# opcode=operator ID
	# sel0 = operator input_strup_0
	# sel1 = operator input_strup_1
	# addr0 = export export_row_0
	# addr1 = export export_row_1
	# selq = import source_tile
	# addr2 = import destination_row

# Where no data value is given in the xml negative infinity is inserted as a recognisable default
# Where n NULL data value is given in the xml positive infinity is inserted as a recognisable default
# Where selX is -1 in the xml, set it to it's local strip/tile value as a matter of default
# Where addrX is -1 in the xml, set it to the same as the implied address (the row number). In the case of addr2(the specified address to write a result to), this will mean addr2 is NOT written to.

#### #Defined parameters
## OLD opcodes
#opcode_dict= {"ADD_I4" : "000001","SUBTRACT_I4": "000010","MULTIPLY_I4": "000011","DIVIDE_I4": "000100","COPY_I4": "000101","MAX_I4": "000110","MIN_I4": "000111","GT_I4": "001000","LT_I4": "001001","EQT_I4": "001010","ADD_R4": "110110","SUBTRACT_R4": "110111","MULTIPLY_R4": "111000","DIVIDE_R4": "111000","COPY_R4": "111010","MAX_R4": "111011","MIN_R4": "111100","GT_R4": "111101","LT_R4": "111110","EQT_R4": "111111","BRANCH_F": "011111","BRANCH_T": "011111","NOP_I4": "000000","NOP_R4": "000000","HALT": "000000"}
## NEW opcodes
opcode_dict= {"ADD_F4" : "000000","SUBTRACT_I4": "000001","MULTIPLY_I4": "000011","DIVIDE_I4": "000100","COPY_I4": "000101","MAX_I4": "000110","MIN_I4": "000111","GT_I4": "100100","LT_I4": "001100","EQT_I4": "010100","ADD_R4": "000000","SUBTRACT_R4": "000001","MULTIPLY_R4": "000011","DIVIDE_R4": "000100","COPY_R4": "000101","MAX_R4": "000110","MIN_R4": "000111","GT_R4": "100100","LT_R4": "001100","EQT_R4": "010100","BRANCH_F": "001000","BRANCH_T": "001000","NOP_I4": "000010","NOP_R4": "000010","HALT": "111111","COPY_OUT_R4":"001001"}
doc = xml.dom.minidom.parse("../xml/input.xml")

count_nops = 0 #Counter holding the number of times a strip has to be filled with T_NOP instructions (i.e the number of potential operations not used)
#### MAIN ####
header_info = doc.getElementsByTagName("map").item(0)

DROWS=int(header_info.getAttribute("n_rows"))
IROWS=int(header_info.getAttribute("end_row"))
TILES=int(header_info.getAttribute("n_tiles"))
STRIPS=int(header_info.getAttribute("n_strips"))
print "File header info: "
print "	Number of tiles:",TILES
print "	Number of strips per tile:",STRIPS
print "	Number of instruction rows per strip:",IROWS
print "	Number of data rows per strip:",DROWS

#Initialise files for storing results:
a = gf.initialise_files(STRIPS,TILES)
zI=a[0]#Array of handles on instruction files: zI[tile][strip]
zD =a[1] #Array of handles on data files: zD[tile][strip]
zA=a[2]
count = 0

#tree[ROW][TILES][STRIPS][INSTRUCTION][DATA0][DATA1]
tree=[[["INSTRUCTION","DATA"]*STRIPS]*TILES]*DROWS

ir_index=0
dr_index=0
t_index=0
s_index=0
for row in doc.getElementsByTagName("row"):
		r=int(row.getAttribute("id"))
#		print "Row: ",r, "ir_index:", ir_index
		t_index=0
		for tile in row.getElementsByTagName("tile"):
				t=int(tile.getAttribute("id"))
#				print "		Tile: ",t, "t_index", t_index

				#Check that the tile value currently being read is the next one in numerical order
				#If it's not the tiles and strips with in them must have a TRUE_NOP inserted
				#Create inputs for a T_NOP operation //For where the xml supplies nothing for certain locations in hydra
				while t_index < t:
						#Creat this T_NOP for every strip in the tile
						for k in range(0,STRIPS):	
								
								count_nops = count_nops+1

								data=FP.fp_infinity(gf.D_wf,gf.D_we,1)	#Set NULLs to negative infinity in the current format as a recognisable default
								H_data=gf.bin_to_hex(data)
								H_data=gf.formatH_for_roach(H_data)

								Dword="Address %d:"%(ir_index) + H_data
								zD[t_index][k].write(Dword+"\n")	#Write the word to file
								count = count+1
								
								opcode=opcode_dict["NOP_I4"]
								#Set sel's to it's local strip/tile value as a matter of default which is the purpose of the index parameters
								sel0=gf.sel_string(-1, k) 
								sel1=gf.sel_string(-1, k)
								
								#Set addresses to the same as the implied address (the row number)
								#In the case of addr2, this will mean addr2 is NOT written to making it a TRUE_NOP 
								addr0=gf.addr_string(-1,ir_index)
								addr1=gf.addr_string(-1,ir_index)
								
								selq=gf.sel_string(-1,t_index)
								addr2=gf.addr_string(-1,ir_index)
								
								instruction_bin=addr2+selq+opcode+sel1+sel0+addr1+addr0
								i_wordH = gf.bin_to_hex(instruction_bin)
								i_wordHF = gf.formatH_for_roach(i_wordH)
								Iword=instruction_bin+":"+i_wordHF
								
								zI[t_index][k].write(Iword+"\n")	#Write the word to file

						t_index = t_index+1

				s_index=0
				for strip in tile.getElementsByTagName("strip"):
						s=int(strip.getAttribute("id"))
#						print "			Strip: ",s, "s_index: ",s_index
				
						#Check that the strip value currently being read is the next one in numerical order
						#If it's not the tiles and strips with in them must have a TRUE_NOP inserted
						#Create inputs for a T_NOP operation //For where the xml supplies nothing for certain locations in hydra
						while s_index < s:

								count_nops = count_nops+1

								data=FP.fp_infinity(gf.D_wf,gf.D_we,1)	#Set NULLs to negative infinity in the current format as a recognisable default
								H_data=gf.bin_to_hex(data)
								H_data=gf.formatH_for_roach(H_data)
								Dword="Address %d:"%(ir_index) + H_data
								zD[t_index][s_index].write(Dword+"\n")	#Write the word to file
								count = count+1
								
								opcode=opcode_dict["NOP_I4"]
								#Set sel's to it's local strip/tile value as a matter of default which is the purpose of the index parameters
								sel0=gf.sel_string(-1, s_index) 
								sel1=gf.sel_string(-1, s_index)
								
								#Set addresses to the same as the implied address (the row number)
								#In the case of addr2, this will mean addr2 is NOT written to making it a TRUE_NOP 
								addr0=gf.addr_string(-1,ir_index)
								addr1=gf.addr_string(-1,ir_index)
								
								selq=gf.sel_string(-1,t_index)
								addr2=gf.addr_string(-1,ir_index)
								
								instruction_bin=addr2+selq+opcode+sel1+sel0+addr1+addr0
								i_wordH = gf.bin_to_hex(instruction_bin)
								i_wordHF = gf.formatH_for_roach(i_wordH)
								Iword=instruction_bin+":"+i_wordHF
								
								zI[t_index][s_index].write(Iword+"\n")	#Write the word to file

								s_index = s_index+1

						operator = strip.getElementsByTagName("operator").item(0)
						exporter = strip.getElementsByTagName("export").item(0)
						importer = strip.getElementsByTagName("import").item(0)
					
						#Capture components and create instruction:
						#Opcode
						opcodeT=operator.getAttribute("id")
						opcode=opcode_dict[opcodeT]
#						print "t%ds%dr%d"%(t,s,r), ": ",opcodeT,":",opcode

						#If selX is set to -1, set it to it's local strip/tile value as a matter of default which is the purpose of the index parameters
						sel0=gf.sel_string(int(operator.getAttribute("input_strip_0")), s_index) 
						sel1=gf.sel_string(int(operator.getAttribute("input_strip_1")), s_index)
					
						#If addrX is set to -1, set it to the same as the implied address (the row number)
						#In the case of addr2, this will mean addr2 is NOT written to 
						addr0=gf.addr_string(int(exporter.getAttribute("export_row_0")),ir_index)
						addr1=gf.addr_string(int(exporter.getAttribute("export_row_1")),ir_index)

						selq=gf.sel_string(int(importer.getAttribute("source_tile")),t_index)
						addr2=gf.addr_string(int(importer.getAttribute("destination_row")),ir_index)

						instruction_bin=addr2+selq+opcode+sel1+sel0+addr1+addr0
						i_wordH = gf.bin_to_hex(instruction_bin)
						i_wordHF = gf.formatH_for_roach(i_wordH)
						Iword=instruction_bin+":"+i_wordHF
						
						zI[t_index][s_index].write(Iword+"\n")	#Write the word to file
				
						#Capture and format data
						dataIn=str(operator.getAttribute("value"))
						printdata=str(operator.getAttribute("value"))
						data_name=str(operator.getAttribute("output"))
						if dataIn == "NULL":
								data=FP.fp_infinity(gf.D_wf,gf.D_we,0)	#Set NULLs to positive infinity in the current format as a recognisable default	
						else:
								data=float(dataIn)
								data=FP.custom_floating_point_creator(data,gf.D_wf,gf.D_we)

						H_data=gf.bin_to_hex(data)
						F_data=gf.formatH_for_roach(H_data)
						Dword="Address %d:"%(ir_index) + F_data

						print "t%ds%dr%d"%(t,s,r), ": ",data_name,": ", printdata, " >> ", dataIn," >> ",F_data
					
						zD[t_index][s_index].write(Dword+"\n")	#Write the word to file
						count = count+1

						s_index= s_index+1
				
				#Check that the strip value currently being read is the next one in numerical order
				#If it's not the tiles and strips with in them must have a TRUE_NOP inserted
				#Create inputs for a T_NOP operation //For where the xml supplies nothing for certain locations in hydra
				while s_index < STRIPS:
						data=FP.fp_infinity(gf.D_wf,gf.D_we,1)	#Set NULLs to negative infinity in the current format as a recognisable default
						H_data=gf.bin_to_hex(data)
						H_data=gf.formatH_for_roach(H_data)
						Dword="Address %d:"%(ir_index) + H_data
						zD[t_index][s_index].write(Dword+"\n")	#Write the word to file
						count = count+1
						
						opcode=opcode_dict["NOP_I4"]
						#Set sel's to it's local strip/tile value as a matter of default which is the purpose of the index parameters
						sel0=gf.sel_string(-1, s_index) 
						sel1=gf.sel_string(-1, s_index)
						
						#Set addresses to the same as the implied address (the row number)
						#In the case of addr2, this will mean addr2 is NOT written to making it a TRUE_NOP 
						addr0=gf.addr_string(-1,ir_index)
						addr1=gf.addr_string(-1,ir_index)
						
						selq=gf.sel_string(-1,t_index)
						addr2=gf.addr_string(-1,ir_index)
						
						instruction_bin=addr2+selq+opcode+sel1+sel0+addr1+addr0
						i_wordH = gf.bin_to_hex(instruction_bin)
						i_wordHF = gf.formatH_for_roach(i_wordH)
						Iword=instruction_bin+":"+i_wordHF
						
						zI[t_index][s_index].write(Iword+"\n")	#Write the word to file

						s_index = s_index+1
				
				
				t_index = t_index+1

		#Check that the tile value currently being read is the next one in numerical order
		#If it's not the tiles and strips with in them must have a TRUE_NOP inserted
		#Create inputs for a T_NOP operation //For where the xml supplies nothing for certain locations in hydra
		while t_index < TILES:
				#Creat this T_NOP for every strip in the tile
				for k in range(0,STRIPS):

						count_nops = count_nops+1

						data=FP.fp_infinity(gf.D_wf,gf.D_we,1)	#Set NULLs to negative infinity in the current format as a recognisable default
						H_data=gf.bin_to_hex(data)
						H_data=gf.formatH_for_roach(H_data)
						Dword="Address %d:"%(ir_index) + H_data
						zD[t_index][k].write(Dword+"\n")	#Write the word to file
						count = count+1
						
						opcode=opcode_dict["NOP_I4"]
						#Set sel's to it's local strip/tile value as a matter of default which is the purpose of the index parameters
						sel0=gf.sel_string(-1, k) 
						sel1=gf.sel_string(-1, k)
						
						#Set addresses to the same as the implied address (the row number)
						#In the case of addr2, this will mean addr2 is NOT written to making it a TRUE_NOP 
						addr0=gf.addr_string(-1,ir_index)
						addr1=gf.addr_string(-1,ir_index)
						
						selq=gf.sel_string(-1,t_index)
						addr2=gf.addr_string(-1,ir_index)
						
						instruction_bin=addr2+selq+opcode+sel1+sel0+addr1+addr0
						i_wordH = gf.bin_to_hex(instruction_bin)
						i_wordHF = gf.formatH_for_roach(i_wordH)
						Iword=instruction_bin+":"+i_wordHF
						
						zI[t_index][k].write(Iword+"\n")	#Write the word to file

				t_index = t_index+1
		ir_index = ir_index+1

gf.close_files(STRIPS,TILES,zI,zD,zA)
print "Count of data words: ", count
print "Count of T_NOPs insterted: ", count_nops










