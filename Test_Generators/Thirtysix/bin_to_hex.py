#!/usr//bin/python2.6
#Reads in the supplied file and converts the binary string on each line into a hexidecimal string and writes it out


####Converts a string of binary characters to a string of hexedecimal characters##########
def bin_to_hex (vec):
		count = 0 
		interim = 0
		j = 0
		k = ""
		e= 3
		z = len(vec)/4+(len(vec)%4) # length of vec once extended to be divisible by 4
		result = range(0,z)
		if len(vec)%4 != 0:
			g = range(0,4-len(vec)%4)
			for w in range(0,len(g)):
							k = k+"0"
			vec = k+vec

		for i in range(0,len(vec)):
				if vec[i] == '1':
						interim = interim + pow(2,e)
				
				if e == 0:
						e = 3
						result[j]=interim 
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
							result[k] = result[k]

		z = ""
		for w in range(0,len(result)):
				z =z+str(result[w])
		return z 

fr = open('binary_input', 'r')
fw = open('simulation_input','w')


a = fr.readline()
for line in fr:
		print "\nbin: ",line
		print ("\nhex: "+bin_to_hex(line))
		fw.write(bin_to_hex(line)+"\n")
print "Completed"
fr.close()
fw.close()



