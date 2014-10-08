
~~~~~~~~~~~~~~~~~~~
DIRECTIONS FOR USE:
~~~~~~~~~~~~~~~~~~~
 * Use process for running code on ROACH hardware in Fynbos at the CHPC:
	** Programs ROACH with the correct bof file with ./prg_roach.sh by first editing it to name the FPGA image as you wish.
	   This will then;
			> Make a bof file from the ./bofInputs/top_level.bin file
			> Moves and mod the bof file for use
			> Runs ./j.py with the correct flags to program the ROACH
	** ./j.py is a dedicated ROACH programming script customised for the environment in the ACE Lab at CHPC specifically.  It will perform the following operations:
			> Select the correct ROACH board
			> Select the correct boffile for programming
			> Program the FPGA
			> Write the host's 10Gbe IP and Port to the FPGA via the 1Gbe connection
			> Configure the 10Gbe core on the FPGA with the correct IP and port number.
			> Reset the FPGA.
			> Readback the host IP from FPGA.


~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONTENTS OF THIS DIRECTORY:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

DIRECTORIES:
------------
 * bofinputs/ 		--Contains input config files (specific to the ROACH boards hosted at CHPC) and FPGA binary for creating loadable ROACH bof file
 * copybofs/		--A local copy of the bof file generated, files that are actually loaded are hosted on the server Sporty at /srv/roach_boot/etch/boffiles/
 * data_outgoing/	--Contains the data.txt file containing data, instructions and commands to be transmitted to Fynbos
 * data_recieved/	--Contains files of values returned from Fynbos

FILES:
------
 * ./README.txt --This file.
 * j.py		--A configuration script that loads the bof file and configures the network interfaces on ROACH. On completion it readsback the IP for verification and resets the FPGA using the register included in Fynbos for such purpoes.
 * mkbof		--A linux executable that creates a ROACH loadable bof file from the contents of ./bofInputs/
 * mkbof.exe 	--The windows equivalent of mkbof, this can be executed using wine, see prg_raoach.sh and Note_getting_wine_to_makeBof
 * monitor.py 	--A script that optionally resets Fynbos and there after monitor the status register in Fynbos reporting any change in state
 * Note_getting_wine_to_makeBof	--HowTo on installing wine to run mkbof.exe on linux
 * newsend.py 	--A communication script that loads the contents of data_outgoing/data.txt into Fynbos using the prescribed 10GBe IP and port, and listens for returning copy_out data as well as a complete off-load of the Fynbos memories.  The listening function needs to be configured for different number of packet returns depending on the program run.
 * prg_roach.sh	--Combines all the steps necessary to create a bof, move it mod it to the correct location, and run j.py to load ot to the FPGA.  This file require editing to name the bof file
 * rst.py		--A version of monitor.py that only performs a reset
 * status.py	--A script that is run on PowerPC core on the ROACH board monitoring the Fynbos status register in the FPGA over the OPB bus. Even in these close quarters it does not poll the register fast enough to capture all changes but reports all those it detects.




