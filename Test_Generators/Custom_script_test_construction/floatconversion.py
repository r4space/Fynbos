#!/usr/bin/python2.7
#Function version to convert input to float data word
#File to convert decimal values into custom fixed point binary format
#Takes in 2 arguements; 1: Integer portion of value, 2: Decimal portion of value.
import sys
from math import pow, floor
import parameters as p

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
		int_bits = 17
		frac_bits = 15

		a = raw_input("Enter a float: ")

		Input = a.split('.')
		int_in = int(Input[0])
		frac_in =float( "0."+Input[1])

		#Checking conditions on whether or not the number will fit with in the given fixed point format. 
		#Note: these conditions only check for maximum and minimum size constraints and not precision.
		if int_in>65535.999969482421875: #Note python does NOT manage to accurately represent this and so numbers less than 0.0000000001 bigger will not be  caught here
  			print '\033[1;41mInteger portion of number entered is too big to be represented\033[1;m'
		if int_in<-65536:
  			print '\033[1;41mInteger portion of number entered is too small to be represented\033[1;m'
		
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
		d = ""
		e = ""
		for i in range(0,len(x)):
				d = d+str(x[i])

				h = bin_to_hex(x)
		for i in range(0,len(h)):
					e = e+str(h[i])

		result = [e,str(a),x]
		return result

