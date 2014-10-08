#!/usr/bin/env python
import corr, time, struct, sys, logging, socket, optparse

fpga=[]

#Set which ROACH board to use (fantasic.roach, invisible.roach, torch.roach, thing.roach):
roach = ""

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


  options = optparse.OptionParser()
  options.set_usage(sys.argv[0] + " <ROACH_HOSTNAME_or_IP> [options]")
  options.add_option("-r", "--roach", dest="roach", type="str", help="Specify the ROACH board")  
  options.add_option("-b", "--boffile", dest="bof", type="str", help="Specify the bof file to load")           
  options.add_option("-i", "--fpga_ip", dest="fip", type="int", help="Specify the FPGA's IP") 
  options.add_option("-p", "--fpga_port", dest="fport", type="int", help="Specify the FPGA's port") 
  #options.add_option("-m", "--fpga_mac", dest="mac", type="int", help="Specify the FPGA's MAC") 
  options.add_option("-a", "--dest_ip", dest="dip", type="int", help="Specify the IP to send packets to from the FPGA") 
  options.add_option("-o", "--dest_port", dest="dport", type="int", help="Specify the port to send packets to from the FPGA")   

  opts, args = options.parse_args()

  print "Welcome"

  if opts.roach == None:
    roach = raw_input("Specify ROACH Board: ");
  else:
    roach = opts.roach

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

  if opts.bof != None:
    boffile = opts.bof

  if boffile == "":

    for i,j in enumerate(fpga.listbof()):
      print i,j

    bof_choice = raw_input ("Select boffile for programming: ")
    boffile = fpga.listbof()[int(bof_choice)]
    print boffile + " Selected"

  print "------------------------"

  print "Programming FPGA with: " + boffile + " ...",
  sys.stdout.flush()
  dev_str = fpga.progdev(boffile)
  print "ok: device string: " + dev_str

  print "---------------------------"

  if opts.fip == None:
    core_ip = raw_input("Set the FPGA's IP address: ");
  else:
    core_ip = opts.fip

  if opts.fport == None:
    core_port = raw_input("Set the FPGA's port: ");
  else:
    core_port = opts.fport
  #if opts.mac == None:
  #  mac_base = raw_input("Set the FPGA's MAC address: ");
  #else:
  #  mac_base = opts.mac

  if opts.dip == None:
    dest_ip = raw_input("Set the destination IP address: ");
  else:
    dest_ip = opts.dip

  if opts.dport == None:
    dest_port = raw_input("Set the destination port: ");
  else:
    dest_port = opts.dport

  print "Configuring 10Gbe core...",
  sys.stdout.flush()
  fpga.tap_start(tx_core_name,mac_base+core_ip,core_ip,core_port)
  print "done"

  print "---------------------------"

  print "Setting-up destination addresses...",
  sys.stdout.flush()
  fpga.write_int("dest_ip",dest_ip)
  fpga.write_int("dest_port",dest_port)
  print "done"

  print "Resetting cores...",
  sys.stdout.flush()
  fpga.write_int("rst",127)
  fpga.write_int("rst",0)
  print "done"

  print "=========================="

  print "Trying to read dest_ip"
  x = fpga.read_int('dest_ip')
  print "This is x: ",x


exit_clean("Finished, exiting")


