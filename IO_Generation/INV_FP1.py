#!/usr/bin/python2.6
from math import floor, pow
import sys
import generator_functions as gf
#File containg a IEEE compliant custom floating-point value creator.  
#Vlaues are entered as decimal floats and returned as binary strings.

#Takes in the hex floating point value to be converted, the fraction width, the exponent width
#Returns the decimal string representation of custom the floating point value
def custom_floating_point_inverter (fpX,wf,we):

		bias=pow(2,we-1)-1

		#Convert to binary
		bin_strX=gf.hex_to_bin(fpX)
		print "Bin_str",bin_strX

		#Get sign
		sign= bin_strX[0]
		print "sign: ",sign

		#Handle special cases:
		#eZ >> exponent is; 0[all zeros], 1[all 1's], 2[non-special case]
		#mZ >> mantissa is; 0[all zeros], 1[non-special case]

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
						if bin_strX[1+we+i]=='0':
								count0s = count0s+1;

				if count0s == wf: #All bits in mantissa are 0's
						mZ=0
				else:
						mZ=1;

				#Report on special cases
				if eZ==0:
						if mZ==0:#Value is zero:
								return 0.0
						else: #mZ==1 : Denormalized number
								print '\033[1;41mError, denormalized values are not part of the accepted format for hydra\033[1;m'
								return "XXXXXXXXX"
				else: #eZ==1:
						if mZ==0:#Value is infinity
								if sign == '0':
										return "+INF"
								else:
										return "-INF"
						else: #mZ==1: value is not a number
								return "NAN"


		#If not a special case continue as normal
		#Determine exponent
		print "exp bits: ", bin_strX[1:we+1]
		expX=int(dec_expX-bias)
		print "expX: ",expX

		#Multiply out of scientific notation
		print "mant bits: ", bin_strX[we+1:]
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
				return float_value
		else:
				return "-"+str(float_value)


######### Main ##########
wf=int(sys.argv[1])
we=int(sys.argv[2])
bias=pow(2,we-1)-1

print "All conversions will be carried out assuming a fraction/mantissa width of %dbits, an exponent width of %dbits and a bias of %d"%(wf,we,bias)
print("Enter a hex formatted floating point value or 'q' to quit")

while (1):
		FP=str(raw_input("Enter a hex value: "))
		if FP=='q':
				sys.exit()
		if len(FP)*4 != (we+wf+1):
				print "Error, value entered is not compatable with format defined: 1 %d %d"%(we,wf)
		else:
				decFP=custom_floating_point_inverter(FP,wf,we)
				
				if type(decFP) == str:
						print FP," = ", decFP
				else:
						print FP," = ",'%30.25g' %decFP
