----------------------------------------------------------------------------------
-- Create Date: 21/10/2010 
-- Project: Parameterised
-- Module Name: End strip
-- Description: Module connecting contents of a strip together into a strip
-- Revision: 0.01 - File Created
-- Additional Comments: Special strip module in that it is the final strip in the tile and therefore has no carry in signal
						--It also has a division enabled operator
----------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.all;
--use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;
-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity END_strip is
		generic (ID : std_logic_vector((STRIPS_Ad_bits+TILES_Ad_bits-1) downto 0));--:= "000001");
		Port ( 
				clk			: in std_logic;
				ins_ctrl 	: in  std_logic_vector (2 downto 0);
				ins_data 	: in  std_logic_vector (DATA_SIZE_C-1 downto 0);
				ins_addr 	: in  std_logic_vector (INS_ADDR_C-1 downto 0);
				
				dataS_aXes	: in other_strips_data;		
				dataS_bXes	: in other_strips_data;		
				dataT_Xes	: in other_tiles_data;

				dataCy_out	: out std_logic_vector(DATA_SIZE_C-1 downto 0) ;	--carry out

				doutT  		: out std_logic_vector(DATA_SIZE_C-1 downto 0) ;	--Eventually to corrosponding strips in other tiles after being sorted
				doutS_a 	: out std_logic_vector(DATA_SIZE_C-1 downto 0) ;	--To other strips A
				doutS_b 	: out std_logic_vector(DATA_SIZE_C-1 downto 0) ;	--To other strips B

				done_o   	: out std_logic_vector(1 downto 0)
			);
end END_strip;

architecture Behavioral of END_strip is

		--inputs
		signal ins_ctrl_s 	: std_logic_vector (2 downto 0);
		signal ins_addr_s 	: std_logic_vector (INS_ADDR_C-1 downto 0);
		signal instruction_s: std_logic_vector (INSTR_WIDTH_C-1 downto 0);              

		signal dataS_aXes_s : other_strips_data;--Data in from other strip A
		signal dataS_bXes_s : other_strips_data;--Data in from other strip B
		signal dataT_Xes_s	: other_tiles_data;--Date in from corrosponding strips in other tiles

			
		--outputs
		signal 	done_slv 		: std_logic_vector(1 downto 0);
		signal	dataCy_o_s	: std_logic_vector (DATA_SIZE_C -1 downto 0);	--carry out

		--internal
		signal off_load_s 	: std_logic;
		signal sel0_s 		: std_logic_vector(STRIPS_Ad_bits-1 downto 0);                   
		signal sel1_s 		: std_logic_vector(STRIPS_Ad_bits-1 downto 0);
		signal selq_s 		: std_logic_vector(TILES_Ad_bits-1 downto 0);
		signal opcode_s 	: std_logic_vector (OPCODE_C-1 downto 0);
		signal CE_s 		: std_logic;
		signal nd_s 		: std_logic;
		signal en0_s 		: std_logic;
		signal en1_s 		: std_logic;
		signal en2_s 		: std_logic;
		signal en3_s 		: std_logic;
		signal addr0_s 		: std_logic_vector (DREGS_Ad_bits-1 downto 0);
		signal addr1_s 		: std_logic_vector (DREGS_Ad_bits-1 downto 0);
		signal addrq1_s 	: std_logic_vector (DREGS_Ad_bits-1 downto 0);
		signal addrq2_s 	: std_logic_vector (DREGS_Ad_bits-1 downto 0);
		signal ins_data_s	: std_logic_vector (DATA_SIZE_C-1 downto 0);

		signal dout0_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal dout1_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal din0_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal din1_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal MUX1_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal MUX2_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);
		signal MUX3_s		: std_logic_vector (DATA_SIZE_C-1 downto 0);

		signal Q_s			: std_logic_vector (DATA_SIZE_C-1 downto 0);

		signal MUX1_sB : std_logic_vector(DATA_SIZE_C-1 downto 0);
		signal MUX2_sB : std_logic_vector(DATA_SIZE_C-1 downto 0);
		signal off_load_sB 	: std_logic;
		signal off_load_sBB 	: std_logic;
--------------------------------------------------------------------------------------------		
		component decoder is
			generic ( Dstrip_ID : std_logic_vector (STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0));
			Port (
					clk			:	in  std_logic;
					ins_ctrl_i 	: 	in  std_logic_vector (2 downto 0);
				   	ins_addr_i 	: 	in  std_logic_vector (INS_ADDR_C-1 downto 0);
				  	done_i 		:	in  std_logic;
				   	instruction_i :	in  std_logic_vector (INSTR_WIDTH_C-1 downto 0);
				   	
				   	off_load_o 	: 	out  std_logic;
				   	sel0_o 		:	out  std_logic_vector(STRIPS_Ad_bits-1 downto 0);
				   	sel1_o 		:	out  std_logic_vector(STRIPS_Ad_bits-1 downto 0);
				   	selq_o 		:	out  std_logic_vector(TILES_Ad_bits-1 downto 0);
				   	opcode_o 	:	out  std_logic_vector (OPCODE_C-1 downto 0);
				   	CE_o 		:	out  std_logic;
				   	en0_o 		:	out  std_logic;
				   	en1_o 		:	out  std_logic;
				   	en2_o 		:	out  std_logic;
				   	en3_o 		:	out  std_logic;
				   	nd_o	 	:	out  std_logic;
				   	addr0_o 	:	out  std_logic_vector (DREGS_Ad_bits-1 downto 0);
				   	addr1_o 	:	out  std_logic_vector (DREGS_Ad_bits-1 downto 0);
				   	addrq1_o 	:	out  std_logic_vector (DREGS_Ad_bits-1 downto 0);
				   	addrq2_o 	: 	out  std_logic_vector (DREGS_Ad_bits-1 downto 0)
				);
		end component;

--------------------------------------------------------------------------------------------		
		component instr_bram_wrapper is
			generic ( Dstrip_ID : std_logic_vector (STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0));
			Port ( ins_addr_ID  :	in  std_logic_vector (INS_ADDR_CI-1 downto 0);
				   clk          :	in  std_logic;
				   ins_ctrl		:	in std_logic_vector (2 downto 0);
				   ins_data		:	in std_logic_vector (DATA_SIZE_C-1 downto 0);
				   dout         :	out std_logic_vector (INSTR_WIDTH_C-1 downto 0)
				  );
		end component;

--------------------------------------------------------------------------------------------	
		component data_bram_wrapper is
				Port ( addr0 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
				       addr1 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
					   addr2 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
					   addr3 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
					   en0 : in  std_logic;
					   en1 : in  std_logic;
					   en2 : in  std_logic;
					   en3 : in  std_logic;
					   dout0 : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   dout1  : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   din0 : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   din1 : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
					   clk : in std_logic);
		end component;

--------------------------------------------------------------------------------------------		
		component div_operator is
		 port ( a : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        b : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        opcode : in  std_logic_vector (OPCODE_C-1 downto 0);
		        clk : in  std_logic;
		        ce : in  std_logic;
		        nd : in  std_logic;
		        done : out  std_logic_vector(1 downto 0);
		        c : out std_logic_vector (DATA_SIZE_C-1 downto 0)
				);
		end component;

--------------------------------------------------------------------------------------------		
		component operator is
		 port ( a : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        b : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        opcode : in  std_logic_vector (OPCODE_C-1 downto 0);
		        clk : in  std_logic;
		        ce : in  std_logic;
		        nd : in  std_logic;
		        done : out  std_logic_vector(1 downto 0);
		        c : out std_logic_vector (DATA_SIZE_C-1 downto 0)
				);
		end component;

--------------------------------------------------------------------------------------------		

begin
						   dataT_Xes_s <= dataT_Xes; 
						   doutT 	<= Q_s;

					   --unregistered outputs
						   done_o 	<= done_slv;

Registers: process (clk)
		   begin
				   if rising_edge (clk) then

	 				   --Registered inputs
						   ins_ctrl_s <= ins_ctrl;
						   ins_addr_s <= ins_addr;
						   ins_data_s <= ins_data;

					   --Registered outputs
		   				   dataCy_out <= dataCy_o_s;
--						   done_o 	<= done_slv;

					  --Registered internals
						   MUX1_s <= MUX1_sB;
						   MUX2_s <= MUX2_sB;
						   off_load_s <= off_load_sBB;
						   off_load_sBB <= off_load_sB;

				   end if;
		   end process;

		   --Connections
		   dataS_aXes_s <= dataS_aXes;
		   dataS_bXes_s <= dataS_bXes;

		   doutS_a <= dout0_s;
		   doutS_b <= dout1_s;

		   din1_s <= Q_s;

--------------------------------------------------------------------------------------------		
Decoder0: decoder 
				generic map (Dstrip_ID => ID)
				port map (
							clk => clk,
							ins_ctrl_i => ins_ctrl_s,
							ins_addr_i => ins_addr_s,
							done_i => done_slv(1),
							instruction_i => instruction_s,	
							off_load_o => off_load_sB,
							sel0_o => sel0_s,
							sel1_o => sel1_s,
							selq_o => selq_s,
							opcode_o => opcode_s,
							CE_o => CE_s,
							en0_o => en0_s,
							en1_o => en1_s,
							en2_o => en2_s,
							en3_o => en3_s,
							nd_o => nd_s,
							addr0_o => addr0_s,
							addr1_o => addr1_s,
							addrq1_o => addrq1_s,
							addrq2_o => addrq2_s
						);

--------------------------------------------------------------------------------------------		
Instruction_memory0: instr_bram_wrapper 
					generic map (Dstrip_ID => ID)
					port map(
					ins_addr_ID => ins_addr_s(INS_ADDR_CI-1 downto 0),
					clk => clk,
					ins_ctrl => ins_ctrl_s,
					ins_data =>  ins_data_s,
					dout => instruction_s);

--------------------------------------------------------------------------------------------		
Data_memory0: data_bram_wrapper 
				Port map (
					   addr0 => addr0_s, 
				       addr1 => addr1_s, 
					   addr2 => addrq1_s, 
					   addr3 => addrq2_s, 
					   en0 => en0_s, 
					   en1 => en1_s, 
					   en2 => en2_s, 
					   en3 => en3_s, 
					   dout0 => dout0_s, 
					   dout1  => dout1_s, 
					   din0 => din0_s, 
					   din1 => din1_s, 
					   clk => clk); 

--------------------------------------------------------------------------------------------	
				ifDiv:	if 	NO_DIVS_C > 0 generate
				begin
						DIVoperatorX: div_operator
									port map(
											a => MUX1_s, 
										    b => MUX2_s, 
										    opcode => opcode_s, 
										    clk => clk, 
										    ce => CE_s, 
										    nd => nd_s, 
										    done => done_slv,
										    c => Q_s);
				end generate;
				
				ifNoDiv:	if 	NO_DIVS_C <= 0 generate
				begin
						OperatorX: operator
									port map(
											a => MUX1_s, 
										    b => MUX2_s, 
										    opcode => opcode_s, 
										    clk => clk, 
										    ce => CE_s, 
										    nd => nd_s, 
										    done => done_slv,
										    c => Q_s);
				end generate;

--------------------------------------------------------------------------------------------		
mux2a:
	with ins_ctrl_s(0) select
			din0_s <= MUX3_s when '1',
					 ins_data_s when '0',
					 (others => '-') when others;

--------------------------------------------------------------------------------------------		
mux2b:
	with off_load_s select
			dataCy_o_s <= dout0_s when '0',
						  (others => '-') when others;

--------------------------------------------------------------------------------------------		
MUX1:
--
	MUX1_sB <= dout0_s when sel0_s =  ID(STRIPS_Ad_bits+TILES_Ad_bits-1 downto TILES_Ad_bits) else
	 		  dataS_aXes_s(conv_integer(sel0_s));
-------------------------------------------------------------------------------------------		
MUX2:
	MUX2_sB <= dout1_s when sel1_s =  ID(STRIPS_Ad_bits+TILES_Ad_bits-1 downto TILES_Ad_bits) else 
			   dataS_bXes_s(conv_integer(sel1_s));


--------------------------------------------------------------------------------------------		
MUX3:
	MUX3_s <= Q_s when selq_s =  ID(TILES_Ad_bits-1 downto 0) else 
			  dataT_Xes_s(conv_integer(selq_s));

end Behavioral;
