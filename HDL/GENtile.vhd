
----------------------------------------------------------------------------------
-- Create Date: 13/10/2010 
-- Project: Parameterised
-- Module Name: General tile
-- Description: Module connecting as many strips as specified together into a tile
-- Revision: 0.01 - File Created
-- Additional Comments:
----------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.STD_LOGIC_ARITH.all;
use IEEE.STD_LOGIC_UNSIGNED.all;
use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;
-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity GEN_tile is
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
end GEN_tile;

architecture Behavioral of GEN_tile is
		
		constant ones : std_logic_vector(NO_STRIPS_C-1 downto 0) := (others => '1');
		constant zeros : std_logic_vector(NO_STRIPS_C-1 downto 0) := (others => '0');
		constant d_variable : integer := NO_DIVS_C-NO_STRIPS_C*(NO_TILES_C-1-conv_integer(ID_t)); --How many div strips still to be implimented

		signal ins_ctrl_s		: std_logic_vector (2 downto 0);
		signal ins_addr_s		: std_logic_vector (INS_ADDR_C-1 downto 0);
		signal ins_data_s		: std_logic_vector (DATA_SIZE_C -1 downto 0);

		signal out_array_AXes 	: all_strips_data;
		signal in_arrays_AXes 	: input_arrays_S;
		
		signal out_array_BXes 	: all_strips_data;
		signal in_arrays_BXes 	: input_arrays_S;
		
		signal out_array_TXes 	: all_strips_data;		--Eventually this is an array of one output word from each strip
		signal in_arrays_TXes 	: input_arrays_T;		--Array of arrays of inputs to a strip of corrosponding strips in other tiles data
		
		signal dataCy_out_Xes	: carry_S;
		
		signal done_Xes			: done_array_S_slv;
		signal overflow_o_s 		: std_logic;
		signal done_o_s 		: std_logic;

		component gen_strip is
		generic (ID : std_logic_vector((STRIPS_Ad_bits+TILES_Ad_bits-1) downto 0));--:= "000"&ID_t);
		Port ( 
				clk			: in std_logic;
				ins_ctrl 	: in  std_logic_vector (2 downto 0);
				ins_data 	: in  std_logic_vector (DATA_SIZE_C-1 downto 0);
				ins_addr 	: in  std_logic_vector (INS_ADDR_C-1 downto 0);

				dataS_aXes	: in other_strips_data;		
				dataS_bXes	: in other_strips_data;		
				dataT_Xes	: in other_tiles_data;

				dataCy_in  	: in std_logic_vector(DATA_SIZE_C-1 downto 0);	--carry in
				dataCy_out	: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--carry out
		
				doutT  		: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--To corrosponding strips in other tiles
				doutS_a 	: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--To other strips A
				doutS_b 	: out std_logic_vector(DATA_SIZE_C-1 downto 0); --To other strips B

				done_o   	: out std_logic_vector(1 downto 0)
			);
		end component;
		
		--Division strip
		component DIV_strip is
		generic (ID : std_logic_vector((STRIPS_Ad_bits+TILES_Ad_bits-1) downto 0));--:= "000"&ID_t);
		Port ( 
				clk			: in std_logic;
				ins_ctrl 	: in  std_logic_vector (2 downto 0);
				ins_data 	: in  std_logic_vector (DATA_SIZE_C-1 downto 0);
				ins_addr 	: in  std_logic_vector (INS_ADDR_C-1 downto 0);

				dataS_aXes	: in other_strips_data;		
				dataS_bXes	: in other_strips_data;		
				dataT_Xes	: in other_tiles_data;

				dataCy_in  	: in std_logic_vector(DATA_SIZE_C-1 downto 0);	--carry in
				dataCy_out	: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--carry out
		
				doutT  		: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--To corrosponding strips in other tiles
				doutS_a 	: out std_logic_vector(DATA_SIZE_C-1 downto 0);	--To other strips A
				doutS_b 	: out std_logic_vector(DATA_SIZE_C-1 downto 0); --To other strips B

				done_o   	: out std_logic_vector(1 downto 0)
			);
		end component;

begin

		--Tile port connections
			--incoming
				ins_data_s <= ins_data;
				ins_addr_s <= ins_addr;
				ins_ctrl_s <= ins_ctrl;
				dataCy_out_Xes(NO_STRIPS_C) <= dataCy_inT;
				in_arrays_TXes <= inter_tile_sorted;
			
			--outgoing
				inter_tile_unsorted	<= out_array_TXes;
			   	done_o <= done_o_s&overflow_o_s;
				dataCy_outT <= dataCy_out_Xes(0);

--				process (clk)
--				begin
--						if rising_edge(clk) then
--						   	done_o <= done_o_s&overflow_o_s;
--						end if;
--				end process;

		label1: for i in 0 to (NO_STRIPS_C-1) generate--i goes to each strip and generates all inputs for that strip before moving on
		begin
				lable2: for j in 0 to (NO_STRIPS_C-1) generate--j goes through the outputs from all the strips and selects which ones it wants to include as an input for the current strip (i)
				begin
						lable3: if (j/=i) generate
						begin
								in_arrays_AXes(i)(j) <= out_array_AXes(j);
								in_arrays_BXes(i)(j) <= out_array_BXes(j);
						end generate;
						lable4: if (j=i) generate
						begin
								in_arrays_AXes(i)(j) <= (others => '-');
								in_arrays_BXes(i)(j) <= (others => '-');
						end generate;
				end generate;
		end generate;

		--Generate strips as division capable or not as needed
		dvariable_GTEz:	if d_variable >= 0 generate
		begin
				--More div strips needed than can fit in this tile
				dvariable_GTS: if d_variable >= NO_STRIPS_C generate
				begin
						DIVstrips: for i in 0 to (NO_STRIPS_C-1) generate
						begin
									DIVstripX: DIV_strip
											generic map (ID => conv_std_logic_vector(i,STRIPS_Ad_bits)&ID_t)
											port map(clk => clk,
													ins_ctrl => ins_ctrl_s,
													ins_data => ins_data_s,
													ins_addr => ins_addr_s,
											
													dataS_AXes => in_arrays_AXes(i),
													dataS_BXes => in_arrays_BXes(i),
													dataT_Xes => in_arrays_TXes(i),	
													
													dataCy_in => dataCy_out_Xes(i+1),
													dataCy_out => dataCy_out_Xes(i),
													doutT => out_array_TXes(i), 		
													doutS_a => out_array_AXes(i),	
													doutS_b => out_array_BXes(i),
													done_o(1) => done_Xes(1)(i),
													done_o(0) => done_Xes(0)(i)
													);
						end generate; --End DIVstrips
				end generate; --End dvariable_GTS
				
				--All remaining div_strips can fit in this tile
				dvariable_LTS: if d_variable < NO_STRIPS_C generate
				begin
						GENstrips:	for i in 0 to (NO_STRIPS_C-1-d_variable) generate	
						begin
								GENstripX: GEN_strip
										generic map (ID => conv_std_logic_vector(i,STRIPS_Ad_bits)&ID_t)
										port map(clk => clk,
												ins_ctrl => ins_ctrl_s,
												ins_data => ins_data_s,
												ins_addr => ins_addr_s,
						
												dataS_AXes => in_arrays_AXes(i),
												dataS_BXes => in_arrays_BXes(i),
												dataT_Xes => in_arrays_TXes(i),	
												
												dataCy_in => dataCy_out_Xes(i+1),
												dataCy_out => dataCy_out_Xes(i),
												doutT => out_array_TXes(i), 		
												doutS_a => out_array_AXes(i),	
												doutS_b => out_array_BXes(i),
												done_o(1) => done_Xes(1)(i),
												done_o(0) => done_Xes(0)(i)
												);
								end generate; --End GENstrips

						DIVstrips: for i in (NO_STRIPS_C-d_variable) to (NO_STRIPS_C-1) generate
						begin
									DIVstripX: DIV_strip
											generic map (ID => conv_std_logic_vector(i,STRIPS_Ad_bits)&ID_t)
											port map(clk => clk,
													ins_ctrl => ins_ctrl_s,
													ins_data => ins_data_s,
													ins_addr => ins_addr_s,
											
													dataS_AXes => in_arrays_AXes(i),
													dataS_BXes => in_arrays_BXes(i),
													dataT_Xes => in_arrays_TXes(i),	
													
													dataCy_in => dataCy_out_Xes(i+1),
													dataCy_out => dataCy_out_Xes(i),
													doutT => out_array_TXes(i), 		
													doutS_a => out_array_AXes(i),	
													doutS_b => out_array_BXes(i),
													done_o(1) => done_Xes(1)(i),
													done_o(0) => done_Xes(0)(i)
													);
						end generate; --End DIVstrips
				end generate; --End dvariable_LTS
		end generate; --End dvariable_GTEz

		dvariable_LTz: if d_variable<0 generate
		begin
				GENstrips:	for i in 0 to (NO_STRIPS_C-1) generate	
				begin
						GENstripX: GEN_strip
								generic map (ID => conv_std_logic_vector(i,STRIPS_Ad_bits)&ID_t)
								port map(clk => clk,
										ins_ctrl => ins_ctrl_s,
										ins_data => ins_data_s,
										ins_addr => ins_addr_s,
				
										dataS_AXes => in_arrays_AXes(i),
										dataS_BXes => in_arrays_BXes(i),
										dataT_Xes => in_arrays_TXes(i),	
										
										dataCy_in => dataCy_out_Xes(i+1),
										dataCy_out => dataCy_out_Xes(i),
										doutT => out_array_TXes(i), 		
										doutS_a => out_array_AXes(i),	
										doutS_b => out_array_BXes(i),
										done_o(1) => done_Xes(1)(i),
										done_o(0) => done_Xes(0)(i)
										);
						end generate; --End GENstrips
		end generate; --End dvariable_LTz

		--AND all done signals together
			done_o_s <= '1' when done_Xes(1) = ones else '0';  
			overflow_o_s <= '0' when done_Xes(0) = zeros else '1';  

end Behavioral;

