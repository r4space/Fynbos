#!/usr/bin/python2.6
#function to convert input to int data word
import parameters as p
import sys
from math import pow

######Decimal integer to binary#############
def Intdec_to_bin (int_in,int_bits):
		a = range(0,int_bits)
		for i in range(0,len(a)):
				a[i] = 0

		k = int_in
		i = int_bits -1
		while k != 0:
				a[i] = k%2
				k = k/2
				i = i-1

		return a

#####Invert binary##########################
def invert_vector (vec):
		output  = range(0,len(vec))
		for k in range(0,len(vec)):

				if vec[k] == 0:
						output[k] = 1
				else:
						output[k] = 0
		return output

####Add 1 to a binary vector################
def bin_add_one (vec):
		output  = vec
		t = 0
		for k in range(len(vec)-1,-1,-1):
				if vec[k] == 0:
						output[k] = 1
						break
				else:
						if t == 0:
							output[k] = 0
							t= 1
						else:
							output[k] = 0
		return output

####Convert binary to Hexidecimal##########
def bin_to_hex (vec):
		count = 0 
		interim = 0
		j = 0
		e= 3
		z = len(vec)/4+(len(vec)%4) # length of vec once extended to be divisible by 4
		result = range(0,z)
		if len(vec)%4 != 0:
			g = range(0,4-len(vec)%4)
			for w in range(0,len(g)):
							g[w] = 0
			vec = g+vec


		for i in range(0,len(vec)):
				if vec[i] == 1:
						interim = interim + pow(2,e)
				
				if e == 0:
						e = 3
						result[j] = interim 
						j = j+1
						interim = 0
				else:
						e = e-1

				count = count +1

		for k in range(0, len(result)):
						if result[k] == 10:
							result[k] = "A"
						elif result[k] == 11:
							result[k] = "B"
						elif result[k] == 12:
							result[k] = "C"
						elif result[k] == 13:
							result[k] = "D"
						elif result[k] == 14:
							result[k] = "E"
						elif result[k] == 15:
							result[k] = "F"
						else:
							result[k] = int(result[k])
		return result

###Print vec###############################
def print_vec (vec):
		d = ""
		for i in range(0,len(vec)):
				d = d+str(vec[i])
		print d


##Decimal to custom Integer binary conversion:
def myint ():
		i = 0
		input = raw_input("Enter an Int: ")
		int_in = int(input)
		#print "int",int_in
		if int_in>2147483647:
				print "Number too big"

		int_bits =32 
		x= Intdec_to_bin (abs(int_in),int_bits)
		#print "binary of int",int_in,":",z

		##Convert to 2's comp if neg:
		if input[0][0] == '-':
			#invert array
			a = invert_vector(x)

			#binary_add one
			x = bin_add_one(a)

		##Print result
		d = ""
		e = ""
	#	print "2's complement of",input,", in 32bits:",
		for i in range(0,len(x)):
				d = d+str(x[i])
	#	print d

	#	print "len x",len(x)
		h = bin_to_hex(x)
	#	print "Result in hex",
		for i in range(0,len(h)):
					e = e+str(h[i])
	#	print e
		result = [e,str(input),x]
		return result

