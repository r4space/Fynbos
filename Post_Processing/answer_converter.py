#!/usr/bin/python2.6
import FP_creator as FP
import generator_functions as gf
import sys

ff=str(sys.argv[1])
fin = open(ff,"r")
LINES=fin.readlines()
#RESULT = range(0,len(LINES))
#for i in range(0,len(LINES)):
#		RESULT[i]=LINES[i].split()
#
#for i in range(0,len(LINES)):
#		for j in range(0,len(RESULT[i])):
#				print "J: ",j
#				binary=FP.custom_floating_point_creator(float(RESULT[i][j]),27,8)
#				RESULT[i][j]=gf.bin_to_dec(binary)
#		
#		fout.write(LINES[i]+"\n")
#		fout.write("\t"+str(RESULT[i])+"\n")
#		fout.write("-----------------------------------------------------------------------------\n")

for i in range (len(LINES)):
		res=FP.custom_floating_point_inverter(LINES[i][8:-1],gf.D_wf ,gf.D_we)
		print res

fin.close()

#print "Completed successfully"

