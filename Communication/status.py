#!/usr/bin/env python
#a script for monitoring the status register directly from borph
import commands

r = commands.getoutput("hd -x /proc/548/hw/ioreg/status_r")
print "this is r: ",r
res = r[10:21]
print"\n this is res: ", res

ser = res

while 1:
	r = commands.getoutput("hd -x /proc/548/hw/ioreg/status_r")
	res = r[10:21]
	if res !=ser:
		print"Current status is: ", res
		ser = res

