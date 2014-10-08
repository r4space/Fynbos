#!/usr/bin/python2.6
#File containing the function version of float1.py to convert input to float data word
#File to convert decimal values into custom fixed point binary format
#Takes in 2 arguements; 1: Integer portion of value, 2: Decimal portion of value.
from test_parameters import *
import sys
from math import pow, floor

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

#####Decimal fraction to binary##############
def Fracdec_to_bin (frac_in,frac_bits):
		
		f = frac_in
		b = range(0,frac_bits)
		for l in range (0,frac_bits):
				t = int(floor(f*2))
				f = f*2
				if t==1:
						b[l] = 1
						f = f - 1
				else:
						b[l] = 0
		return b 

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
###Function to take an array and make into a readable continuous string
def printable_vec (vec):
		e= ""
		for i in range(0,len(vec)):
					e = e+str(vec[i])
		return e



####Function to create float#################Decimal to custom fixed point binary conversion:
def myreal():
		i = 0
		a = raw_input("Enter a float: ")

		Input = a.split('.')
		int_in = int(Input[0])
		frac_in =float( "0."+Input[1])

		#Checking conditions on whether or not the number will fit with in the given fixed point format. 
		if int_in>(pow(2,(int_bits-1))-1): #>(2^19) -1 = 524287
				print '\033[1;41mInteger portion of number is too big, exiting\033[1;m'
				sys.exit(0);

		if int_in<-1*(pow(2,int_bits-1)): #<-2^19 = -524288
				print '\033[1;41mInteger portion of number is too negative, exiting\033[1;m'
				sys.exit(0);
		
		if frac_in <pow(2,-1*frac_bits): #<2^-16
				print '\033[1;41mFraction is too small and will be rounded to zero\033[1;m'
		
		if frac_in >0.999984741211: #<2^-16
				print '\033[1;41mFraction is too big and should be rounded to one nut will be rounded to the maximum fraction\033[1;m'
		
		#Should also have some checks on the negative fractional inputs just haven't bothered so far 
		
		z= Intdec_to_bin (abs(int_in),int_bits)
		y = Fracdec_to_bin(frac_in, frac_bits)

		x = z+y

		##Convert to 2's comp if neg:
		if Input[0][0] == '-':
			#invert array
			b = invert_vector(x)

			#binary_add one
			x = bin_add_one(b)
		
		##Print result
		e = ""
		h = bin_to_hex(x)
		for i in range(0,len(h)):
					e = e+str(h[i])

		result = [e,str(a),x]
		return result

