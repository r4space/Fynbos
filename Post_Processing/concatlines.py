#!/usr/bin/python2.6
import sys

a=str(sys.argv[1])
b = int(sys.argv[2])
f = open(a,"r")

x =f.readline().rstrip('\n')
x=x.replace(' ','')
newline = x
while newline:
		for i in range(b-1):
				x =f.readline().rstrip('\n')
				x=x.replace(' ','')	#Removes excess whitespace
				newline = newline+" "+x

		print newline
		x =f.readline().rstrip('\n')
		x=x.replace(' ','')
		newline = x

