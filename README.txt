
~~~~~~~~~~~~~~~~~~~
DIRECTIONS FOR USE:
~~~~~~~~~~~~~~~~~~~
 * The contents of this directory all relate to the FPGA implemented Fynbos architecture
 * Things to be edited when changing Fynbos configurations:
 	** Scripts:
		IO_generation/generator_functions.py
		post_processing/generator_functions.py
	** Fynbos:
		VHDL/hydra_parameters.vhd
		IP/ip_pcore_dir/br_converter.xco	--And the core needs regenerating after editing this file.

~~~~~~~~~~~~~~~~~~~~~~~~~~~
CONTENTS OF THIS DIRECTORY:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

DIRECTORIES:
------------
 * ./Communication/	-- All scripts and config files pertaining to loading a Fynbos image, and loading and running a program in the image on a ROACH board.
 * ./HDL/ --Contains the VHDL files that represent a Fynbos for use on ROACH (Exmple IP cores and ISE or Vivado project files which would go with these to create a ROACH ready bit stream can be found in the Hardware_Test projects folder in the next directory above.)
 * ./IO_Generation/ -- All scripts pertaining to creating load files of data and instructions targeted at a Fynbos image. The README.txt in this folder also contains instructions on how to generate a load file from an xml program file 
 * ./Post_Processing/
 * ./Test_Generators/ -- Scripts for generating, packaging, and evaluating tests for Fynbos such as, memory, interconnect, branching, or mathematics. The outputs of such include hardware and simulator input files.


FILES:
------
 * ./README.txt --This file.


