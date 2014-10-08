#!/usr/bin/python2.6
import math as m
#File containing functpons used to generate hydra testbenches
#Set hydra system parameter here to be used by all other scripts that call this one.
DROWS =2048	#Number of data registers per strip
IROWS =1024	#Number of execution rows and also the number of instruction registers per strip
STRIPS = 8	#Number of strips per tile
TILES = 8	#Number of tiles
div_strips = 0	#Number of strips with division capabilities
DADDR_BITS = 11	#Number of bits used to address a register
IADDR_BITS = 10	#Number of bits used to address a register
SC_len = 36		#Number of bits in a system command
D_len = 36		#Number of bits in a data word
###### Creates and opens a seperate file for each strip containing it's instructions and another one for it's data######
#Returns a 2element array where the 1st element is an array of the handles to all the instruction files arranged into their tiles and the second is the same for the data and answer files.
#Files are named as follows: If_<tile>_<strip>, Df_<tile>_<strip>, Af_<tile>_<strip>
# Z=[zI,zD, zA
#zI=[TILES[STRIPS instruction files handles]]
#zD=[TILES[STRIPS data files handles]]
#zA=[TILES[STRIPS answer files handles]]
def initialise_files (strips,tiles):
		Ifiles=range(0,tiles)	
		Dfiles=range(0,tiles)	
		Afiles=range(0,tiles)	
		zI=range(0,tiles)
		zD=range(0,tiles)
		zA=range(0,tiles)
		s=0 #strip id
		t=0 #tile id

		for t in range(0,tiles):
				Ifiles[t]=range(0,strips)
				Dfiles[t]=range(0,strips)
				Afiles[t]=range(0,strips)
				
				zI[t]=range(0,strips)
				zD[t]=range(0,strips)
				zA[t]=range(0,strips)

				for s in range(0,strips):
						#Create files
						Ifiles[t][s]="../outputs/instructions/If_%d_%d" %(t,s)
						Dfiles[t][s]="../outputs/data/Df_%d_%d" %(t,s)
						Afiles[t][s]="../outputs/answers/Af_%d_%d" %(t,s)

						#Create handles to access files
						zI[t][s]="I_S%dT%d" %(t,s)
						zD[t][s]="D_S%dT%d" %(t,s)
						zA[t][s]="A_S%dT%d" %(t,s)
						
						#Open files and attache to handles
						zI[t][s]=open(Ifiles[t][s],"w")
						zD[t][s]=open(Dfiles[t][s],"w")
						zA[t][s]=open(Afiles[t][s],"w")

		Z=[zI, zD, zA]
		return Z

###### Closes all the files opend using initialise_files()######
#returns nothing
def close_files (strips,tiles,zI,zD):
		s=0 #strip id
		t=0 #tile id

		for t in range(0,tiles):
				for s in range(0,strips):
						zI[t][s].close()
						zD[t][s].close()

		return

###### Decimal integer to binary string#############
#Takes in a signed integer and the number of bits to be used
#Returns a 2's complement binary string representation
def int_to_bin (int_in,int_bits):
		#Convert to a binary string
		a = range(0,int_bits)
		for i in range(0,len(a)):
				a[i] = 0

		k = abs(int_in)
		i = int_bits -1
		while k != 0:
				a[i] = k%2
				k = k/2
				i = i-1
		vec=''.join(map(str,a))

		#Check if the value is negative and if so convert to 2's complement
		if str(int_in)[0] =='-':
				#Invert string:
				invert = range(0,len(vec))
				for j in range(0,len(vec)):
						if vec[j] == 0:
								invert[j] = 1
						else:
								invert[j] = 0
				#Add 1 in binary:
				t = 0
				comp  = invert
				for l in range(len(invert)-1,-1,-1):
						if invert[l] == 0:
								comp[l] = 1
								break
						else:
								if t == 0:
									comp[l] = 0
									t= 1
								else:
									comp[l] = 0
				vec=comp

		return vec

####Convert a binary string of anylength into a Hexidecimal string##########
#returns a string
def bin_to_hex (string):
		count = 0 
		interim = 0
#	z = (len(string)/4)+(4-(len(string)%4)) # length of vec once extended to be divisible by 4

		#Z=length of resulting hex string
		
		if len(string)%4==0:
				z=len(string)/4
		else:
				z=len(string)/4+1

		result = range(0,z)
		j=0

		if len(string)%4 != 0:
			g = range(0,4-len(string)%4)
			ext=''
			for w in g:
					ext=ext+'0'

			ext=''.join(map(str,ext))
							
			string = ext+string

		for i in range(0,len(string),4):
				if string[i]=='1':
						interim=8
				if string[i+1]=='1':
						interim=interim+4
				if string[i+2]=='1':
						interim=interim+2
				if string[i+3]=='1':
						interim=interim+1

				result[j]=interim
				interim=0
				j=j+1


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

		result = ''.join(map(str,result))	
		return result

####Format a hexidecimal string of any length to be a roach compliant 64bit word######
#returns a string
def formatH_for_roach(hstring):
		#Expand to 64bits:
		z=16-len(hstring)
		for i in range(0,z):
				hstring="0"+hstring

		#insert hex markers:
		hstring_new=""
		for i in range(0,16,2):
				hstring_new=hstring_new+"\\x"+hstring[i:i+2]

		return hstring_new

####Convert an integer value into a roach (64bit) formatted word 
#returns a string
def roach_word(value):

		value=int_to_bin(value,36)		#Convert int value to binary
		value=bin_to_hex(value)			#Convert binary to hex
		dwordH=formatH_for_roach(value)	#Format hex for roach

		return dwordH

####Returns the hydra data address of the number given####
#returns a an array [row, strip, tile] address values in integers
#Takes in an integer value which is a direct count from 0 to the consequtive row in the whole system cummulatively through 0:0:0 to x:x:x
#For data addresses
def hydra_Daddr (sys_Dvalue):

		if (sys_Dvalue>(DROWS*STRIPS*TILES-1) or sys_Dvalue<0):
				print('\033[1;41m address value queried with gf.hydra_Daddr() is not withing the current hydra systems scope\033[1;m')
				return
		else:
				row = sys_Dvalue%DROWS	
				sys_stripth = sys_Dvalue/DROWS		#This is effectively: m.floor(sys_Dvalue/DROWS) = xth strip in the system
				tile = sys_stripth/STRIPS			#This is effectively: m.floor(m.floor(sys_Dvalue/DROWS)/STRIPS)
				strip = sys_stripth - tile*STRIPS	#No. strips in the system up to this one- xth strip this is gives the strip within this tiles
				
				result=[row,strip,tile]

				return result



#For instruction addresses
def hydra_Iaddr (sys_Ivalue):

		if (sys_Ivalue>(IROWS*STRIPS*TILES-1) or sys_Ivalue<0):
				
				print ('\033[1;41m address value queried with gf.hydra_Iaddr() is not withing the current hydra systems scope\033[1;m')
				return
		else:
				row = sys_Ivalue%IROWS
				sys_stripth = sys_Ivalue/IROWS		#This is effectively: m.floor(sys_Dvalue/DROWS) = xth strip in the system
				tile = sys_stripth/STRIPS			#This is effectively: m.floor(m.floor(sys_Dvalue/DROWS)/STRIPS)
				strip = sys_stripth - tile*STRIPS	#No. strips in the system up to this one- xth strip this is gives the strip within this tiles
					
				result=[row,strip,tile]

				return result






#Creates a string of length given of zeros
#Returns a string
def str_of_zeros (length):
		a=""
		while len(a)<length:
				a=a+"0"
		return a

#Create a hydra-compatabile hexidecimal version of a signed integer
##Takes a signed integer and returns a hex string
def int1 (int_in):
		i = 0
		if int_in >pow(2,D_len-1)-1: #>34359738367
				print '\033[1;41mNumber too big, exiting\033[1;m'
				sys.exit(0);
		
		if int_in<(-1*pow(2,D_len-1)): #<-34359738368
				print '\033[1;41mNumber too negative, exiting\033[1;m'
				sys.exit(0);
		
		x= int_to_bin (int_in,D_len)
		
		h = bin_to_hex(x)

		return h

#print("int1 -5: ", int1(-5))
#print("int1 0: ", int1(0))
#print("int1 -0: ", int1(-0))
#print("int1 10: ", int1(10))
#print("int1 12: ", int1(12))
#print("int1 7894560: ", int1(7894560))
#print("int1 -10: ", int1(-10))
#print("int1 -12: ", int1(-12))
#print("int1 -7894560: ", int1(-7894560))
#print("int1 34359738368 : ", int1(34359738368))
#print("int1 34359738367 : ", int1(34359738367))
#print("int1 -34359738368: ", int1(-34359738368))
#print("int1 -34359738367: ", int1(-34359738367))
#print("int1 -34359738369: ", int1(-34359738369))
