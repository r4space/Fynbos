#!/usr/bin/python2.6
#Takes in a hex representation of a FP value and returns the decimal equivalent
#Takes in the hex floating point value to be converted, the fraction width, the exponent width
#Returns the decimal string representation of custom the floating point value
import pprint
import generator_functions as gf
import FP_creator as fpc
import sys


input = sys.argv[1]

res = fpc.custom_floating_point_inverter (input,gf.D_wf,gf.D_we)

print"result: ",res

