CONTENTS OF THIS README:
----------------------
 * Contents of this directory
 * Process required for generating, running, and evaluating a test.

IN THIS DIRECTORY:
------------------
 * Directories:
 	** ./Custom_script_test_construction/ --Contains an interactive script, "instructions.py", that takes an argument of how many statements(rows) worth of data and instructions you would like to generate and returns both the data and hydra-instructions to be loaded into hydra as two ordered arrays, and the command level instructions accompanying such

fixed-point/	--All old fixed-point scripts that were used in the initial stages while fixed-point was being considered as an alternative to the floating-point cores ultimately used
outputs/	--A directory used when creating Fynbos test inputs
paranioa/	--Scripts created towards verifying the Xilinx FP cores according to Paranoia, the work was never completed.
Sixtyfour/	-- Scripts for generating the input for a double precion Fynbos, these are unsophisticated as they were abandoned realtively early on in development
Thirtysix/	-- 36bit word generation scripts and handcoding, these are unsophisticated as they were abandoned realtively early on in development

Files: Are mostly self explanitory
Test generators in the 0 series expect double the number of data rows as instruction rows
Test generators in the 1 series expect the same number of data rows as instruction rows
clean.sh 	--cleans ./outputs
FP_creator.py	--Contains functions required to decimal values into floating-point hex values formatted for Fynbos and the reverse 
generator_functions.py	--Contains more functions and parameters
Inter_comms.py 	--Tests the interconnect on Fynbos
packet_assembler.py 	--Packs data and instructions and answers from the files in ./outputs/ to create a load file for the FPGA and answer file for comparison with the results returned from the FPGA

PROCESSING A TEST:
------------------
1. Check generator_functions.py contains the correct configuration parameters to match the target Fynbos FPGA image being tested.
2. Run  ./clean.sh to remove all previous file in ./outputs
3. Run the selected test file*.  This will generate instructions, data, and operation results according to Tile, Strip, and Row, and store them in ./outputs/
4. Run packet_assembler.py to pack all generated instruction, data, and answer files into data.txt (Instructions, Data, and Fynbos Commands ready for transmission to Fynbos), sim.txt (the same as data.txt but formatted for the ISE simulator), and answer_file containg the operation results.
5. After loading the correct FPGA image, copy data.txt to ../comms/outgoing_data/ and use newsend.py in ../comms/ to transmit the program and recieve the results

6.On recieving results:
	1. Remove any extra communication packets recieved and recorded (for instance there will likely be two packets each of of 3 X"BBBBEEEEAAAADDDD" words and a X"FFFFEEEEAAAADDDD", depending on how the listening is carried out.
	2. There is no need to convert the values to decimal, the hex representation can be directly compared 
	3. The results will be received in the reverse order to which they are compiled in the answers file, therefore for a direct vim -d of the two, one must be reversed. This is done simple with;		$ tac Received_file > reversed_received_file
	4. Similarily, the received results are reported using lower case alphabetical characters, while the scripts that generate the answers could be changed the simplist solution is to highlight the file in vim and us gU to toggel everything to uppercase
	5. Finally, the last word to be off-loaded via the OFF_LOAD state is repeated twice, removing this would require a whole additional state and so was considered an acceptable error as it's simple to remove in post processing

*Note not all test scripts have been updated to handel the parameterised scaling that was retro-fitted to Fynbos, some are hard-wired to a 8x8x4 Fynbos configuration, is such cases the hard-coded STRIP and TILE address bit value of '3' simply needs to be replaced with the parameters in generator_functions.py, namely gf.STRIP_Ad_bits and gf.TIOLES_Ad_bits





