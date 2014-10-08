#!/usr/bin/env python
import corr, time, struct, sys, logging, socket, optparse
import time

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

  print "Resetting cores...",
  sys.stdout.flush()
  fpga.write_int("rst",127)
  time.sleep(1)
  fpga.write_int("rst",0)
  print "done"

  print "=========================="

exit_clean("Finished, exiting")


