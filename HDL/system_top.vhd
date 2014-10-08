----------------------------------------------------------------------------------
-- Create Date: 13/10/2010 
-- Project: Parameterised
-- Module Name: System
-- Description: This is the system top level where ICON, tiles and data interface are all integrated	
-- Revision: 0.01 - File Created
-- Additional Comments: 
-- 	Port and signal naming convetion used:
-- 		dataT_x_y ; x= strip, y = tile, port0
-- 		d_InterTile_XY_s, X = strip, Y = source tile, _s = signal;
--	Status port value interpretation; RESET: 0, COMMAND: 1, LD:2, LI1:3, LI2:4, RUN1:5, RUN2:6, RUN3:7, OF:8, ERROR:9
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.all;
use IEEE.STD_LOGIC_UNSIGNED.all;
use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;
-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity system_top is
    Port ( clk : in  STD_LOGIC;
           reset : in  STD_LOGIC;
           status : out  STD_LOGIC_VECTOR (3 downto 0);
           sim_rx_data : in  STD_LOGIC_VECTOR (63 downto 0);
           sim_rx_valid : in  STD_LOGIC;
		   sim_rx_ack : out std_logic;
           sim_tx_data : out  STD_LOGIC_VECTOR (63 downto 0);
           sim_tx_valid : out  STD_LOGIC;
		   sim_tx_end_of_frame : out std_logic
   		);
end system_top;

architecture Structural of system_top is

		component BR_converter
				 port (
				    a: in std_logic_vector(DATA_SIZE_C-1 downto 0);
					result: out std_logic_vector(IREGS_Ad_bits downto 0)); --This port is 1 bit wider than desired to cater for the sign bit which is unwanted and ignored but which the core gives out
		end component;

		component new_icon is
				port (
				clk 			: in  std_logic;
		    	reset_i 		: in  std_logic;
		  		status_o		: out std_logic_vector (3 downto 0);
		
				rx_data_i		: in std_logic_vector (63 downto 0);
		  		rx_valid_i		: in std_logic;
				rx_ack_o		: out std_logic;

		  		tx_data_o		: out std_logic_vector(63 downto 0);
				tx_valid_o		: out std_logic;
				tx_end_of_frame_o : out std_logic;
		
				ins_ctrl_o		: out std_logic_vector (2 downto 0);	
				ins_data_o		: out std_logic_vector (DATA_SIZE_C-1 downto 0);
		  		ins_addr_o		: out std_logic_vector (INS_ADDR_C-1 downto 0);
				ins_done_i		: in std_logic_vector(1 downto 0);

				CPO_ctrl_i		: in std_logic;
				CPO_data_i		: in std_logic_vector(DATA_SIZE_C-1 downto 0);
		  		
				branch_cont_i	: in std_logic;
				branch_data_i	: in std_logic_vector (IREGS_Ad_bits-1 downto 0);
				dataCy_i		: in std_logic_vector (DATA_SIZE_C-1 downto 0)
				);
		end component;

		component BRCP_tile is
				generic (ID_t : std_logic_vector (TILES_Ad_bits-1 downto 0));
				Port ( clk : in  std_logic;
					   ins_data : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   ins_addr : in  std_logic_vector (INS_ADDR_C-1 downto 0);
					   ins_ctrl : in  std_logic_vector (2 downto 0);
					   inter_tile_sorted	: in input_arrays_T;
					   dataCy_inT : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   dataCy_outT : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   inter_tile_unsorted : out all_strips_data; 
					   done_o : out  std_logic_vector(1 downto 0);
					   CPO_ctrl : out std_logic;
				   	   CPO_data  : out std_logic_vector(DATA_SIZE_C-1 downto 0);	   
				   	   branch_data : out std_logic_vector (DATA_SIZE_C-1 downto 0);
				   	   branch_ctrl : out std_logic
		   			);
		end component;

		component GEN_tile is
				generic (ID_t : std_logic_vector (TILES_Ad_bits-1 downto 0));
				Port ( clk : in  std_logic;
					   ins_data : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   ins_addr : in  std_logic_vector (INS_ADDR_C-1 downto 0);
					   ins_ctrl : in  std_logic_vector (2 downto 0);
					   inter_tile_sorted	: in input_arrays_T;
					   dataCy_inT : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   dataCy_outT : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   inter_tile_unsorted : out all_strips_data; 
					   done_o : out  std_logic_vector(1 downto 0)
			   		);
		end component;

		component END_tile is
				generic (ID_t : std_logic_vector (TILES_Ad_bits-1 downto 0));
				Port ( clk : in  std_logic;
					   ins_data : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   ins_addr : in  std_logic_vector (INS_ADDR_C-1 downto 0);
					   ins_ctrl : in  std_logic_vector (2 downto 0);
					   inter_tile_sorted	: in input_arrays_T;
					   dataCy_outT : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   inter_tile_unsorted : out all_strips_data; 
					   done_o : out  std_logic_vector(1 downto 0)
			   		);
		end component;

	constant ones : std_logic_vector(NO_TILES_C-1 downto 0) := (others => '1');		
	constant zeros : std_logic_vector(NO_TILES_C-1 downto 0) := (others => '0');		

	--NewICON
	 signal reset_s : std_logic := '1';
	 signal status_s : std_logic_vector (3 downto 0) := "0000";	
	
	 signal rx_data_s : std_logic_vector (63 downto 0) := (others => '-');
	 signal rx_valid_s : std_logic:= '0';
	 signal rx_ack_s : std_logic:= '0';
	 
	 signal tx_data_s : std_logic_vector(63 downto 0):= (others => '-');
	 signal tx_valid_s : std_logic := '0';
	 signal tx_end_of_frame_s : std_logic := '0';
	 
	 signal ins_ctrl_s : std_logic_vector (2 downto 0) := "000";	
	 signal ins_data_s : std_logic_vector (DATA_SIZE_C-1 downto 0):= (others => '-');
	 signal ins_addr_s : std_logic_vector (INS_ADDR_C-1 downto 0):= (others => '-');
	 
	 --Tiles
	 signal ins_done_s : std_logic_vector(1 downto 0);

	 signal CPO_ctrl_s : std_logic;
	 signal CPO_data_s : std_logic_vector(DATA_SIZE_C-1 downto 0);
	 signal branch_cont_s : std_logic;
	 signal br_data_converted_s : std_logic_vector (IREGS_Ad_bits-1 downto 0);
	 signal branch_data_s : std_logic_vector (DATA_SIZE_C-1 downto 0);

	 signal collect_unsorted : unsorted_Tiles;
	 signal collection_sorted : sorted_Tiles; 

	 signal dataCy_Xes : carry_T;
	 signal done_Xes : done_array_T_slv;

	 signal s_open : std_logic;
	 
begin
		rx_data_s <= sim_rx_data;
		rx_valid_s <= sim_rx_valid;
		sim_rx_ack <= rx_ack_s;
		sim_tx_data <= tx_data_s;
		sim_tx_valid <= tx_valid_s;
		sim_tx_end_of_frame <= tx_end_of_frame_s;
		reset_s <= reset;
		status <= status_s;

		BR_converterX : BR_converter
				port map (
			            a => branch_data_s,
    	        		result(IREGS_Ad_bits-1 downto 0) => br_data_converted_s,
--						result(IREGS_Ad_bits) => open);
						result(IREGS_Ad_bits) => s_open);

		new_iconX : new_icon 
				port map (clk => clk, 		
						  reset_i => reset_s,
					      status_o => status_s,
					     					
					      rx_data_i => rx_data_s,
					      rx_valid_i => rx_valid_s,
						  rx_ack_o => rx_ack_s,

					      tx_data_o => tx_data_s,
					      tx_valid_o => tx_valid_s,
						  tx_end_of_frame_o => tx_end_of_frame_s,
					      			
					      ins_ctrl_o => ins_ctrl_s,
					      ins_data_o => ins_data_s,
					      ins_addr_o => ins_addr_s,
		
					      ins_done_i => ins_done_s,

						  CPO_ctrl_i => CPO_ctrl_s,
						  CPO_data_i => CPO_data_s,

					      branch_cont_i => branch_cont_s,
					      branch_data_i => br_data_converted_s,
					      dataCy_i => dataCy_Xes(0)
						 );
		
		SORT1: for i in 0 to (NO_TILES_C-1) generate	--i = destination tile
		begin
				SORT2: for j in 0 to (NO_STRIPS_C-1) generate --j = strip input within a collection being made
				begin
						SORT3: for k in 0 to (NO_TILES_C-1) generate --k = source tile output
						begin
								SORT4:if (k/=i) generate
								begin
										collection_sorted(i)(j)(k) <= collect_unsorted(k)(j);
								end generate;
								SORT5: if(k=i) generate
								begin
										collection_sorted(i)(j)(k) <= (others => '1');
								end generate;
						end generate;
				end generate;
		end generate;


		BRCP_TILE_X: BRCP_tile
			generic map (ID_t => conv_std_logic_vector(0,TILES_Ad_bits))
			Port map ( clk => clk,
					   ins_data => ins_data_s,
					   ins_addr => ins_addr_s,
					   ins_ctrl => ins_ctrl_s,
					   inter_tile_sorted => collection_sorted(0),
					   dataCy_inT => dataCy_Xes(1),
					   dataCy_outT => dataCy_Xes(0),
					   inter_tile_unsorted => collect_unsorted(0),
					   done_o(1) => done_Xes(1)(0),
					   done_o(0) => done_Xes(0)(0),
					   CPO_ctrl => CPO_ctrl_s,
					   CPO_data => CPO_data_s,
				   	   branch_data => branch_data_s,
				   	   branch_ctrl => branch_cont_s
	   				);

		MID_TILES_X: for i in 1 to NO_TILES_C-2 generate
				begin
						MID_TILE_X: gen_tile
							generic map (ID_t => conv_std_logic_vector(i,TILES_Ad_bits))	
							port map (clk => clk,		
								 	  ins_data => ins_data_s,
								 	  ins_addr => ins_addr_s,
								 	  ins_ctrl => ins_ctrl_s,
								 	  inter_tile_sorted => collection_sorted(i),
								 	  dataCy_inT => dataCy_Xes(i+1), 		
								 	  dataCy_outT => dataCy_Xes(i),
								 	  inter_tile_unsorted => collect_unsorted(i),
								 	  done_o(1) => done_Xes(1)(i), 
								 	  done_o(0) => done_Xes(0)(i)			  
							  		);
				end generate;
							
		END_TILE_X: END_tile
				generic map (ID_t =>conv_std_logic_vector(NO_TILES_C-1,TILES_Ad_bits))
				Port map ( clk => clk,
						   ins_data => ins_data_s,
						   ins_addr => ins_addr_s, 
						   ins_ctrl => ins_ctrl_s,
						   inter_tile_sorted =>	collection_sorted(NO_TILES_C-1),
						   dataCy_outT => dataCy_Xes(NO_TILES_C-1),
						   inter_tile_unsorted => collect_unsorted(NO_TILES_C-1),
						   done_o(1) => done_Xes(1)(NO_TILES_C-1),
						   done_o(0) => done_Xes(0)(NO_TILES_C-1)
						  ); 
		
				AND_dones: ins_done_s(1) <= '1' when done_Xes(1) = ones else '0'; --AND whole array
				AND_overflows: ins_done_s(0) <= '0' when done_Xes(0) = zeros else '1'; --OR whole array


end Structural;
