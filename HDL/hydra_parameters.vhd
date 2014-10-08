----------------------------------------------------------------------------------
-- Create Date: 13/10/2010 
-- Project: Parameterised
-- Module Name: Hydra parameters
-- Description: Package defining system wide contants, types and functions
-- Revision: 0.01 - File Created
-- Additional Comments:
--Change warnings [CWs] are associated with all constants, these refer to what other parameters should be changed/considered if the given parameter is changed. It is suggested that a search be done for all mentoions of the relevant parameter in this file too, in order to see what parameters consider it as worth a CW
	--BRAM in the vertex5 is in 18bit wide blocks, this must be taken into consideration whenever data path word width(DATA_SIZE_C) is changed which affects a host of subsidary components including and especially the data memory blocks, or if the hydra instruction shape is altered (INSTR_WIDTH_C) which amongst many things will greatly affect how the instruction memory is constructed.
	--Changes to the constants in here will more than likely mean changes are required to the input generating python scripts
	--The maximum number of strips possible is 64.  If this is to be changed, the strip and tile addressing system has to be changed which means the instruction format needs to be re-vamped, such action is not parameterised due to the propegating implications on BRAM configuration and loading procedure 
--At the bottom of this file is a list of things that cannot be changed as they are not, cannot or should not be parameterized see UNCHANGEABLES
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.all;
use IEEE.STD_LOGIC_ARITH.all;
use IEEE.STD_LOGIC_UNSIGNED.all;
--use IEEE.NUMERIC_STD.ALL;
library UNISIM;  
use UNISIM.Vcomponents.all;
package hydra_parameters is

	constant DATA_SIZE_C: integer := 32;	
--	constant IDATA_SIZE_C: integer := 36;	--This is just used for parameterization, in reality, the same pathways are used for data and instruction memory access, just potentially different subsets
	constant NO_TILES_C : integer := 8; --Min = 2
	constant NO_STRIPS_C : integer := 7; --Min = NO_DIVS_C+2 or 3 which ever's smaller ;3 is 2 branch strips and 1 end strip in BRtile
	constant NO_DIVS_C : integer := 4;--Maximum = NO_STRIPS_C*NO_TILES_C-3[BR0,BR1,CPO strips] Minimum = 0
	constant NO_DREGS_C : integer :=1024;
	constant NO_IREGS_C : integer :=1024;

	constant OPCODE_C: integer := 6;	
	constant STRIPS_Ad_bits : integer := 3;	
	constant TILES_Ad_bits : integer := 3;
	constant DREGS_Ad_bits : integer := 10;
	constant IREGS_Ad_bits : integer := 10;
	constant INSTR_WIDTH_C : integer := 45; -- :=REGS_Ad_bits +TILES_Ad_bits +OPCODE_C +STRIPS_Ad_bits +STRIPS_Ad_bits +REGS_Ad_bits +REGS_Ad_bits;

	constant INS_ADDR_CD : integer := 16; -- := DREGS_Ad_bits+STRIPS_Ad_bits+TILES_Ad_bits;	
	constant INS_ADDR_CI : integer := 16; -- := IREGS_Ad_bits+STRIPS_Ad_bits+TILES_Ad_bits;	
	constant INS_ADDR_C : integer := 16; -- := The bigger of the above 2 options
    constant ZERO_ADDRESS   : std_logic_vector(INS_ADDR_C-1 downto 0) := (others => '0');

	constant SC_LEN	: integer	:=35;	--Length of the biggest system command, i.e number of bits needed to represent the bigest of the system commands; LI/LD/RUN/OFLD --INS_ADDR_C+3+number of bits needed to hold total number of values in LI or LD (max)

---------------------------------------------------------------------------------------------
--TYPES
---------------------------------------------------------------------------------------------

		--all_strips_data: Has 3 roles; in each it is an array/collection of one word from each strip within a tile.
		--other_strips_data: The array entering a strip holding all data words from other strips in the local tile, hence it consists of 0 to NO_STRIPS_C-2 words and excludes itself
		--input_arrays_S: An array of arrays: The collection of input array ports for each strip, that is each element is an array of ordered words of data from other strips both in the local tile and remote strips
		--other_tiles_data: Used as the collective input to a strip of words from corrosponding strips in all other tiles.
		--input_arrays_T: The array input to a tile off other_tiles_data arrays (pre-arranged set of elements consisting of arrays of the corrosponding same strip inter-tile words)
		--unsorted_Tiles: Array of the tile outputs from strips, i.e each element of the array is the ordered list of 0 to NO_STRIPS_C-1 words from a tile, the  purpose is an inbetween before the outputs are re-connected(sorted) into new collections of 
		--sorted_Tiles: The collection of input arrays to be fed into each tile and distributed to strips
		--done_array_S: Array holding all the done signals coming out of strips within a tile, whole array is later and'd together
		--done_array_T: Array holding all the done signals coming out of all tiles, whole array is later and'd together
		--carry_S: Array used to connect all the carry through ports between strips
		--carry_S_END: Array used to connect all the carry through ports between strips for the end tile only
		--carry_T: Array used to connect all the carry through ports between tiles

	type all_strips_data is array (0 to NO_STRIPS_C-1) of std_logic_vector(DATA_SIZE_C-1 downto 0);	
	type other_strips_data is array (0 to NO_STRIPS_C-1) of std_logic_vector(DATA_SIZE_C-1 downto 0); 		
	type input_arrays_S is array (0 to NO_STRIPS_C-1) of other_strips_data; 
	type other_tiles_data is array (0 to NO_TILES_C-1) of std_logic_vector(DATA_SIZE_C-1 downto 0);	
	type input_arrays_T is array (0 to NO_STRIPS_C-1) of other_tiles_data;
	type unsorted_Tiles is array (0 to NO_TILES_C-1) of all_strips_data;	
	type sorted_Tiles is array (0 to NO_TILES_C-1) of input_arrays_T; 
	type overflow_array_S is array (0 to NO_STRIPS_C-1) of std_logic; 
	type overflow_array_T is array (0 to NO_TILES_C-1) of std_logic; 
	type done_array_S_slv is array (1 downto 0) of std_logic_vector(0 to NO_STRIPS_C-1);	--done_array_S_slv(1) == done array, (0) ==overflow array 
	type done_array_T_slv is array (1 downto 0) of std_logic_vector (0 to NO_TILES_C-1); 
	
	type carry_S is array (0 to NO_STRIPS_C) of std_logic_vector(DATA_SIZE_C-1 downto 0); 
	type carry_S_END is array (0 to NO_STRIPS_C-1) of std_logic_vector(DATA_SIZE_C-1 downto 0); 
	type carry_T is array (0 to NO_TILES_C-1) of std_logic_vector(DATA_SIZE_C-1 downto 0);

	type main_states is (IDL, CMD, LOAD_DATA, LD_FM, LI1, LI2, LI_FM, RUN1, RUN2, RUN3, OFLD, OFLDFLUSH, FLUSH_O, FLUSH_R);
	type TxRx_states is (idle, WMR, PMR,PTMR, POFLD,CPKT,BTPKT,TPKT);

---------------------------------------------------------------------------------------------
--PROCEDURES
---------------------------------------------------------------------------------------------
	procedure inc_Daddress (signal p_address : inout std_logic_vector (INS_ADDR_CD -1 downto 0));
	procedure dec_Daddress (signal p_address : inout std_logic_vector (INS_ADDR_CD - 1 downto 0); signal numregs : in integer range 2048 downto 0); 

	procedure inc_Iaddress (signal p_address : inout std_logic_vector (INS_ADDR_CI -1 downto 0));
	procedure dec_Iaddress (signal p_address : inout std_logic_vector (INS_ADDR_CI - 1 downto 0)); 

end hydra_parameters;


package body hydra_parameters is

 	procedure inc_Daddress (signal p_address : inout std_logic_vector (INS_ADDR_CD -1 downto 0)) is
		begin
			
				--Last register on this strip, move to next strip
				if (conv_integer(p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits)) = NO_DREGS_C-1) then 
						p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) <= (others => '0');--reg=0

						--Last strip on tile, move to next tile
						if (conv_integer(p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits)) = NO_STRIPS_C-1) then 

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) <= (others => '0');--strip=0

								--If this is the last tile, last strip and last reg then we've reached the end.
								if (conv_integer(p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0))= NO_TILES_C-1) then 

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= (others => '0'); --Tile=0

								else

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0)+1;--inc tile
								end if;
						else
									p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) <= p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits)+1;--inc strip

						end if;
				else
						p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) <= p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) +1; --inc reg 

				end if;

		end procedure inc_Daddress; 

	procedure dec_Daddress (signal p_address: inout std_logic_vector (INS_ADDR_CD - 1 downto 0); signal numregs : in integer range 2048 downto 0) is
		begin
			
				if (p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) = 0) then --last reg
				
					p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) <= conv_std_logic_vector(numregs-1,DREGS_Ad_bits);

						if (p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) = 0) then --last strip

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) <= conv_std_logic_vector(NO_STRIPS_C-1,STRIPS_Ad_bits);

								if (p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) = 0) then --last tile

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= conv_std_logic_vector(NO_TILES_C-1, TILES_Ad_bits);

								else

								p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= p_address(INS_ADDR_CD -1-DREGS_Ad_bits - STRIPS_Ad_bits downto 0) - 1;
								end if;
						else
								p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) <= p_address(INS_ADDR_CD -1-DREGS_Ad_bits downto INS_ADDR_CD-DREGS_Ad_bits-STRIPS_Ad_bits) - 1;
						end if;
				else

						p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) <= p_address(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits)  - 1;
				end if;

		end procedure dec_Daddress; 

 	procedure inc_Iaddress (signal p_address : inout std_logic_vector (INS_ADDR_CI -1 downto 0)) is
		begin
			
				--Last register on this strip, move to next strip
				if (conv_integer(p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits)) = NO_IREGS_C-1) then 
						p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= (others => '0');--reg=0

						--Last strip on tile, move to next tile
						if (conv_integer(p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits)) = NO_STRIPS_C-1) then 

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) <= (others => '0');--strip=0

								--If this is the last tile, last strip and last reg then we've reached the end.
								if (conv_integer(p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0))= NO_TILES_C-1) then 

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= (others => '0'); --Tile=0

								else

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0)+1;--inc tile
								end if;
						else
									p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) <= p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits)+1;--inc strip

						end if;
				else
						p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) +1; --inc reg 

				end if;

		end procedure inc_Iaddress; 

	procedure dec_Iaddress (signal p_address: inout std_logic_vector (INS_ADDR_CI - 1 downto 0)) is
		begin
			
				if (p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) = 0) then 
				
					p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= conv_std_logic_vector(NO_IREGS_C-1,IREGS_Ad_bits);

						if (p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) = 0) then 

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) <= conv_std_logic_vector(NO_STRIPS_C-1,STRIPS_Ad_bits);

								if (p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0) = 0) then 

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits - TILES_Ad_bits downto 0) <= conv_std_logic_vector(NO_TILES_C-1, TILES_Ad_bits);

								else

								p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0) <= p_address(INS_ADDR_CI -1-IREGS_Ad_bits - STRIPS_Ad_bits downto 0) - 1;
								end if;
						else
								p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) <= p_address(INS_ADDR_CI -1-IREGS_Ad_bits downto INS_ADDR_CI-IREGS_Ad_bits-STRIPS_Ad_bits) - 1;
						end if;
				else

						p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= p_address(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits)  - 1;
				end if;

		end procedure dec_Iaddress; 

end hydra_parameters;

--UNCHANGEABLES
--Position, length and settings of command type bits in the header command words (bits 2 downto 0 of command words)
--Length and settings of the ins_ctrl bits
