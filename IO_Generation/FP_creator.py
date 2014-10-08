#!/usr/bin/python2.6
from math import floor
import generator_functions as gf
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

#Wf##Number of fraction bits, width of the fraction
#we##Number of exponent bits, width of the exponent
#bias##=pow(2,we-1)-1, integer value of the bias

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
		first1_index="FRED"
		
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

		if first1_index=="FRED": #No ones were found meaning the value is 0.0
				exponent=0
				normalised=bin_str
				return_array=[exponent,normalised]
				return return_array


		if first1_index!=0: #integer component is zero as first1 must be beyond the 'point' //10.0101 or 0.01011 are the only options

				exponent=0-(first1_index-1)

				normalised="1."
				for i in range(first1_index+1,len(bin_str)):
						
						normalised=normalised+bin_str[i]

		else: #msb in bin_str is a '1' //Not any variant of 0.xyz, has to be 1xyz.abc
				exponent = point_index-1

				normalised="1."
				for i in range(1,len(bin_str)):
						if bin_str[i]=='.': #skip index of the point
								continue
						
						normalised=normalised+bin_str[i]

		return_array=[exponent,normalised]
		return return_array

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

								return fraction[:wf]	#Returns all values up till and including the last one before the truncation point

						else:
								return bin_add_one(fraction[:wf])


		else: #Not in a tie and so can be trunctated

				return fraction[:wf]	#Returns all values up till and including the last one before the truncation point

#Takes in the fraction and exponent width in bits of the current format
#Return the largest (positive OR negative) value that the current format can support, returned as positive here but it's just a sign change for negative
#Return value is in decimal
def fp_max (wf,we):
		#In explination of the below calculation consider the standard single precision FP representation as an example:
			# Max representable value is 1.111......1*2^127 // Implied '1.' followed by a mantissa filled with ones times 2 to Emax
			# Which without the '.' is 24 ones which is equivalent to: 2^24 - 1	//(pow(2,wf+1)-1)
			# To reinsert the '.', it needs to be shifted back by 23 places hence the: *2^-23 //*pow(2,-wf)
			# All timesed by 2 to the maximum exponent: 2^127 //*pow(2,Emax)
		Emax=pow(2,we-1)-1
		maximum = (pow(2,wf+1)-1)*pow(2,-wf)*pow(2,Emax)

		return maximum;

#Takes in the fraction and exponent width in bits of the current format
#Return the smallest (in fractional size positive OR negative)/the highest precision value that the current format can support
#Return value is in decimal
def fp_precision (wf,we):
		#In explination of the below calculation consider the standard single precision FP representation as an example:
		# The highest precision representable value is 1.000...0*2^Emin //The implied '1.' followed by a mantissa of zeros times 2 to Emin
		# It cannot be a value represented as 0.something as such numbers are denormalized which isn't suipported by the Xilinx cores
		Emin=-(pow(2,we-1)-2)
		precise_value = 1*pow(2,Emin)
		return precise_value;

#Takes in the fraction and exponent width in bits of the current format as well as the desired sign
#The sign is represented with an integer 1(-) or 0(+) as desired
#Returns the Floating-point standard representation for the correctly signed infinity in the current bit format
#Return value is as a hex string in the current FP format
def fp_infinity(wf,we,sign):

		mantissa = ""
		for i in range(0,wf):
				mantissa=mantissa+"0"

		exponent = ""
		for i in range(0,we):
				exponent=exponent+"1"

		infinity=str(sign)+exponent+mantissa

		return infinity;

#Takes in the decimal real value to be converted, the fraction width, the exponent width, the exponent bias
#Returns the binary string representation of custom the floating point value
def custom_floating_point_creator (decX,wf,we):

		mx=fp_max(wf,we)
		if decX>=mx:
				print '\033[1;44The value returned is the representation of infinity\033[1;m'
		
		zeros="0000000000000000000000000000000000000000000000000000000000000000"#64 zeros
		bias=pow(2,we-1)-1

		#Get sign
		if decX < 0:
				sign=1
		else:
				sign=0

		#Create binary representation
		binary_string = dec_to_bin(decX)
		normalised_array = normalise(binary_string)

		#Create exponent and convert to binary
		exp = normalised_array[0]
		
		#Check exponent is within a valid range
		if exp > bias:
				print '\033[1;41mNumber is too large, requiring an exponent of %d where only vlaues up to %d are supported\033[1;m'%(exp,bias)
				sys.exit()

		if exp<(-1*(bias-1)):
				print '\033[1;41mNumber is too small, requiring an exponent of %d where only values down to %d are supported.  Denormalized numbers are not supported.\033[1;m'%(exp, bias-1)
				sys.exit()

		#Handle special case of exp = 0 (meaning either the value is zero or the value doesn't need to be shifted
		if exp == 0 and normalised_array[1][0]=='0':#Then the whole value is zero and so the exponent is set to all zeros
				bin_exp=gf.int_to_bin(exp,we)
		
		else:#Normal case so bias the exponent before converting to binary
				exp = exp+bias
				bin_exp=gf.int_to_bin(exp,we)

		#Round off mantissa if need be:
		significand=normalised_array[1][2:]	#Mantissa with the "1." cut off the front

		if len(significand)>wf:	#If the length of the significand is longer than wf then it needs to be rounded off.

				significand=sround(significand,wf)
				print '\033[1;42m Number %g has been rounded\033[1;m' %decX

		else: #Buffer with zeros to make up full mantissa

				buff = wf-len(significand)
				significand = significand+zeros[0:buff]

		#Format into one floating-point representation string:
		fp_value=str(sign)+bin_exp+significand

		return fp_value



#Takes in the hex floating point value to be converted, the fraction width, the exponent width
#Returns the decimal string representation of custom the floating point value
def custom_floating_point_inverter (fpX,wf,we):

		bias=pow(2,we-1)-1

		#Convert to binary
		bin_strX=gf.hex_to_bin(fpX)

		#Get sign
		sign= bin_strX[0]

		#Handle special cases:
		#eZ >> exponent is; 0[all zeros], 1[all 1's], 2[non-special case]
		#mZ >> mantissa is; 0[all zeros], 1[only last bit is a 1 meaning*] 2[non-special case]

		#Check exponent
		dec_expX=gf.bin_to_dec(bin_strX[1:we+1])
		if dec_expX == 0: #Exponent is all 0's
				eZ=0
		elif dec_expX == (pow(2,we)-1): #Exponent is all 1's
				eZ =1
		else: #Not a special case
				eZ=2;

		#Check mantissa
		if eZ != 2: #Only do if a special case

				count0s =0
				for i in range(wf):
						if bin_strX[we+i+1]=='0':
								count0s = count0s+1

				if count0s == wf: #All bits in mantissa are 0's
						mZ=0
				elif count0s == 1 and bin_strX[wf-1]=='1': #Special case of mantissa is all zeros except the last bit
						mZ=1
				else:
						mZ=2;

				#Report on special cases
				if eZ==0:
						if mZ==0:#Value is zero:
								return 0.0
						elif mZ ==1:	#Logical TRUE, or could be a denormalised number but unlikely as they shouldn't be getting created in any case
								return "TRUE"
						else: #mZ==2 : Denormalized number
								print '\033[1;41mError, denormalized values are not part of the accepted format for hydra\033[1;m'
								return "XXXXXXXXX"
				else: #eZ==1:
						if mZ==0:#Value is infinity
								if sign == '0':
										return "+INF"
								else:
										return "-INF"
						else: #mZ==1 or 2: value is not a number
								return "NAN"


		#If not a special case continue as normal
		#Determine exponent
		expX=dec_expX-bias

		#Multiply out of scientific notation
		mantissaX=bin_strX[we+1:] 

		bin_value ="1"+ mantissaX #Mantissa with the implied one added on in front

		if expX>=wf:#Add zeros onto the end
				for i in range(expX-wf):
						bin_value=bin_value+"0"

		elif expX<wf and expX>0: #Place the point in the correct location, all bits already present
				bin_value = bin_value[0:expX+1]+"."+bin_value[expX+1:]
		
		elif expX<0: #Add zeros and the point infront of the value
				for i in range(int(abs(expX)-1)):
						bin_value = "0"+bin_value
				bin_value = "0."+bin_value
		elif expX==0:
				bin_value=bin_value[0]+"."+bin_value[1:]
	
		#Convert binary to decimal
		float_value = gf.bin_to_dec(bin_value)
		if sign == '0':
				return str('%25.18g' %float_value)
		else:
				return str('-%25.18g' %float_value)

