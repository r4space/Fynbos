#!/usr/bin/python2.6
import sys
from math import floor
#File containg a IEEE compliant custom floating-point value creator.  
#Vlaues are entered as decimal floats and returned as binary strings.

#Define system:
#Terminology:
#	exponent: E => The value stored in the exponent bits as an unsigned integer
#	fraction: frac => The field of the significand that lies to the right of its implied binary point
#	biased exponent: e=E+bias => Actual decimal exponent
#	precision: p => The number of significant bits, this is frac+implied 1 eg 24 for single precision
#	Maximum exponent: Emax
#	Minimum exponent: Emin

input = sys.argv[1]
wf = int(input)			##Number of fraction bits, width of the fraction
input = sys.argv[2]
we = int(input)			##Number of exponent bits, width of the exponent
bias=pow(2,we-1)-1 		## Integer value of the bias

######Decimal real to binary#############
#Takes in a float value
#Returns a string containing the binary value
def dec_to_bin (decimal):
		a=""
		b=""

		i = int(abs(decimal))	#Get truncated integer portion
		f = abs(decimal)%1		#Get fractional portion


		#Convert integer to binary
		if i == 0:
				a="0"
		else:
				while i != 0:
						a =str(i%2)+a
						i = i/2

		#Convert fraction to binary
		if f == 0:
				b = "0"
		else:
				while f !=0:
						t = int(floor(f*2))
						f = f*2
						if t==1:
								b= b+"1"
								f = f - 1
						else:
								b=b+"0"

		binary= a+"."+b
		return binary

######Binary string to a normalised binary string with an exponent#############
#Takes in a binary float string
#Returns an array of 2, index 0 contains the exponent and index 1 the normalised binary string
def normalise (bin_str):

		normalised=""
		
		#Find the point
		for i in range(len(bin_str)):
				if bin_str[i]=='.':
						point_index = i
						break;

		#Find the 1st '1'
		for i in range(len(bin_str)):
				if bin_str[i]=='1':
						first1_index = i
						break;

		if first1_index==0: #msb in bin_str is a '1'

				exponent = point_index-1

				normalised="1."
				for i in range(1,len(bin_str)):
						if bin_str[i]=='.': #skip index of the point
								continue
						
						normalised=normalised+bin_str[i]

		else: #integer component it zero

				exponent=0-(first1_index-1)

				normalised="1."
				for i in range(first1_index,len(bin_str)):
						
						normalised=normalised+bin_str[i]


		return_array=[exponent,normalised]
		return return_array

#Takes in the actual/real-life exponent and the bias and prints an error message if the exponent is unrepresentable
#Note, method assumes the bias is calculated according to bias=pow(2,We-1)-1 and denormalized numbers are not supported
#Returns a binary string representing the floating point biased exponent
def create_exponent(exp,bias,we):
		#Check exponent is within a valid range
		if exp > bias:
				print '\033[1;41mNumber is too large, requiring an exponent of %d where only vlaues up to %d are supported\033[1;m'%(exp,bias)
		if exp<(-1*(bias-1)):
				print '\033[1;41mNumber is too small, requiring an exponent of %d where only values down to %d are supported.  Denormalized numbers are not supported.\033[1;m'%(exp, bias-1)
		
		#Convert value to binary
		exp_s=""
		FPexp = exp+bias
		for i in range(0,we):
				exp_s=str(FPexp%2)+exp_s
				FPexp=FPexp/2

		return exp_s

#Takes in a binary string 
#Returns the same binary string with 1 added to it
def bin_add_one (bin_str):
		t=0 
		#Create a vector:
		vec=range(len(bin_str))
		for i in range(len(bin_str)):
				vec[i]=bin_str[i]

		for k in range(len(bin_str)-1,-1,-1):#Range from end of string to 0
				if bin_str[k]=='0':
						vec[k]='1'
						break
				else:
						if t == 0:	#No 1 carried yet, carry a 1 from now on until it can be placed
								vec[k]='0'
								t=1		
						else:	#Already carrying a one
								vec[k]='0'
						
						if k==0: #If you've run through the whole string without finding a single 0 you're overflowing 
								print '\033[1;41mWhile rounding the mantissa it overflowed\033[1;m'
								print '\033[1;41mThis value will NOT be correctly represented and will cause serious errors!!!!\033[1;m'

		#Return vector to a string:
		new_bin_str=""
		for i in range(len(vec)):
				new_bin_str=new_bin_str+vec[i]
	
		return new_bin_str

#Takes in a binary string and the width of the resturn value
#Returns most significant bits of the inputted string but rounded to fit into the width supplied
def sround (fraction,wf):
		zeros="0000000000000000000000000000000000000000000000000000000000000000"#64 zeros

		if fraction[wf]=='1': #In a tie or requires rounding up based on examining the 1st bit BEYOND the truncation point


				if fraction[wf-1]=='1': #Needs rounding up based on examining the last bit to be included

						return bin_add_one(fraction[:wf])


				else: #Even and either needs rounding up(not in a tie) or truncating(in a tie and already even)

						if fraction[wf+1:]==zeros[0:len(fraction[wf+1:])]:

								return fraction[:fraction]	#Returns all values up till and including the last one before the truncation point

						else:
								return bin_add_one(fraction[:wf])


		else: #Not in a tie and so can be trunctated

				return fraction[:wf]	#Returns all values up till and including the last one before the truncation point


#Takes in the decimal real value to be converted, the fraction width, the exponent width, the exponent bias
#Returns the binary string representation of custom the floating point value
def custom_floating_point_creator (decX,wf,we,bias):
		
		zeros="0000000000000000000000000000000000000000000000000000000000000000"#64 zeros

		#Get sign
		if decX <= 0:
				sign=1
		else:
				sign=0
	
		#Create binary representation
		binary_string = dec_to_bin(decX)
		normalised_array = normalise(binary_string)

		#Create exponent and convert to binary
		bin_exp=create_exponent(normalised_array[0],bias,we)

		#Round off mantissa if need be:
		significand=normalised_array[1][2:]	#Mantissa with the "1." cut off the front

		if len(significand)>wf:	#If the length of the significand is longer than wf then it needs to be rounded off.

				significand=sround(significand,wf)
				print '\033[1;41mNumber has been rounded\033[1;m'

		else: #Buffer with zeros to make up full mantissa

				buff = wf-len(significand)
				significand = significand+zeros[0:buff]

		#Format into one floating-point representation string:
		fp_value=str(sign)+bin_exp+significand

		return fp_value

print("Enter a floating point value or 'q' to quit")
while (1):
		a=raw_input("Enter a floating point value: ")
		if str(a)=='q':
				sys.exit()
		a=float(a)
		result = custom_floating_point_creator (a,wf,we,bias)
		print result


