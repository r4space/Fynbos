#!/usr/bin/python2.6
#File to convert decimal values into custom fixed point binary and hex formats
#Takes in 2 arguements; 1: Integer portion of value, 2: Decimal portion of value.
#Eg:Convert value  -123.456 to binary/hex
#	$ ./float1 -123.456

import sys
from math import pow, floor

int_bits = 20
frac_bits = 16

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



##Decimal to custom fixed point binary conversion:
i = 0
input = sys.argv[1].split('.')
int_in = int(input[0])
frac_in =float( "0."+input[1])
print "int",int_in
print "frac",frac_in

if int_in>(pow(2,(int_bits-1))-1): #>(2^19) -1 = 524287
		print '\033[1;41mInteger portion of number is too big, exiting\033[1;m'
		sys.exit(0);

if int_in<-1*(pow(2,int_bits-1)): #<-2^19 = -524288
		print '\033[1;41mInteger portion of number is too negative, exiting\033[1;m'
		sys.exit(0);

if frac_in <pow(2,-1*frac_bits): #<2^-16
		print '\033[1;41mFraction is too small and will be rounded to zero\033[1;m'
		print("fracin: ",frac_in)

if frac_in >0.999984741211: #<2^-16
		print '\033[1;41mFraction is too big and should be rounded to one nut will be rounded to the maximum fraction\033[1;m'

################Should also have some checks on the negative fractional inputs just haven't bothered so far 

z= Intdec_to_bin (abs(int_in),int_bits)
y = Fracdec_to_bin(frac_in, frac_bits)
#print "binary of abs(%d)"%(int_in),":",z
#print "bin of frac",frac_in,":",y

x = z+y

##Convert to 2's comp if neg:
if input[0][0] == '-':
	#invert array
	a = invert_vector(x)
#	print "inverted word:", a
	
	#binary_add one
	x = bin_add_one(a)
#	print "2's complement: ",x

##Print result
d = ""
e = ""
for i in range(0,len(x)):
		d = d+str(x[i])

print "int",d[0:20]
print "frac",d[20:36]
print "Result in binary:", d

h = bin_to_hex(x)
print "Result in hex",
for i in range(0,len(h)):
			e = e+str(h[i])
print e

