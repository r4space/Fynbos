Generating a load file:
1. Check generator_functions.py contains the correct configuration parameters to match the target Fynbos FPGA image being tested.
2. Run  ./clean.sh to remove all previous file in ./outputs
3. check the correct *.xml file has been copied to ./xml/input.xml
4. Run ./compiler.py This will extract the program instructions, and data values from the xml and store them in ./outputs/
5. Run packet_assembler.py to pack all instruction and data into ./outputs/data.txt (Instructions, Data, and Fynbos Commands ready for transmission to Fynbos), sim.txt (the same as data.txt but formatted for the ISE simulator).
6. After loading the correct FPGA image, copy ./outputs/data.txt to ../comms/outgoing_data/ and use newsend.py in ../comms/ to transmit the program and recieve the results.

7.On recieving results (to be found in ../comms/received_data/Received_results):
	1. Remove any extra communication packets received and recorded. If results were copied out during execution a tail communication packet containg 3 X"BBBBEEEEAAAADDDD" words followed by a X"FFFFEEEEAAAADDDD" will represent the end of copied out data. A second packet of the same nature will also end the off loaded memory contents if requested. Also the last word to be off loaded will have been repeated, one instance of which can therefore be deleted.
	2. Once refined of such, copy the result file into ../post_processing/ and run ./hex_inverter.py on it to convert the values to decimal.

istr_length_compile.py	--Edit to put in Fynbos target parameters (strip, tile, div counts and memory depths), and it will output the other required paramters that cannot be easily calculated in VHDL and so much be entered.

float1.py   --Takes in an argument of a decimal float and returns the hex equivalent in hydra's custom 32bit fixed-point number representation, handles n    eg numbers too
int1.py     --Takes in an argument of a decimal integer and returns the hex equivalent in hydra's 32bit representation, handles neg numbers too
 
Process to generate  
