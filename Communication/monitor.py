#!/usr/bin/env python
import corr, time, struct, sys, logging, socket, optparse
import time

try:
		resetQ = int(sys.argv[1])
except:
		print "This script expects a value (0 or 1) when run, \n1 = reset\n0 = no reset"
		print "Please try again"
		exit()

fpga=[]

#Set which ROACH board to use (fantasic.roach, invisible.roach, torch.roach, thing.roach):
roach = "192.168.100.100"

#Set which bof file is programmed onto the FPGA, if left empty you will be prompted to chose from a list:
boffile = ""

#Define the 10Gbe core's IP address and listening port:
core_ip=10*(2**24) + 11
core_port=3157

#Define destination IP address and port:
dest_ip  =10*(2**24) + 1
dest_port=3158

#The MAC for the core is generated based on the following and the assigned IP:
mac_base=(2<<40) + (2<<32)

#Name of the 10Gbe core, will be displayed in ifconfig on the ROACH board:
tx_core_name = "gbe0"

def exit_clean(msg):
  try:
    for f in fpgas: f.stop()
  except: pass
  print msg
  exit()

if __name__ == "__main__":
  lh=corr.log_handlers.DebugLogHandler()
  logger = logging.getLogger(roach)
  logger.addHandler(lh)
  logger.setLevel(10)

  print "Welcome"

  print("Connecting to server %s... "%(roach)),
  try:
    fpga = corr.katcp_wrapper.FpgaClient(roach, logger=logger)
  except:
    print "problem connecting to: " + roach + ". Exiting"
    exit (-1)
  time.sleep(2)
  if fpga.is_connected():
    print "ok\n"
  else:
    print "ERROR connecting to server %s.\n"%(roach)
    exit(-1)

  if resetQ == 1:
		  print "Resetting cores...",
  		  sys.stdout.flush()
  		  fpga.write_int("rst",4294967295) #2^32-1
  		  x = fpga.read_int('status_r')
  		  time.sleep(1)
  		  z = fpga.read_int('status_r')
  		  fpga.write_int("rst",0)
  		  k = fpga.read_int('status_r')
  		  print "done"

  print "=========================="

  print "Trying to read status: "
  y = fpga.read_int('status_r')

  z= fpga.read_int('dest_ip')
  print "IP: ", z
  print "IP_bin",bin(z)

  y1 = fpga.read_int('status_r')
  y=y1
  print "The status is now: ",bin(y1),"\n", hex(y1), "here: ", y1

  while (1):
		y1 = fpga.read_int('status_r')
		
		if y1 != y:

			print "The status is now: ",y1, "\n",bin(y1),"\n", hex(y1)
			y = y1

exit_clean("Finished, exiting")


