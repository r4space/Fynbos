----------------------------------------------------------------------------------
-- Create Date: 26/10/2010 
-- Project: Parameterised
-- Module Name: Strip decoder
-- Description: Control system inside each strip which decodes and distributes the instruction loaded
-- Revision: 0.01 - File Created
-- Additional Comments:
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.all;
use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity BRdecoder is
   	generic (Dstrip_ID : std_logic_vector (STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0));-- := "010010");

	Port (
			clk			:	in std_logic;
			ins_ctrl_i 	: 	in  STD_LOGIC_VECTOR (2 downto 0);
			ins_addr_i 	: 	in  STD_LOGIC_VECTOR (INS_ADDR_C-1 downto 0);
			done_i 		:	in  STD_LOGIC;
			instruction_i :	in  STD_LOGIC_VECTOR (INSTR_WIDTH_C-1 downto 0);
			 
			 off_load_o : 	out  STD_LOGIC;
			 sel0_o 	: 	out  std_logic_vector(STRIPS_Ad_bits-1 downto 0);
			 sel1_o 	: 	out  std_logic_vector(STRIPS_Ad_bits-1 downto 0);
			 selq_o 	: 	out  std_logic_vector(TILES_Ad_bits-1 downto 0);
			 opcode_o	:	out  STD_LOGIC_VECTOR (OPCODE_C-1 downto 0);
			 CE_o 		:	out  STD_LOGIC;
			 en0_o 		:	out  STD_LOGIC;
			 en1_o 		:	out  STD_LOGIC;
			 en2_o 		:	out  STD_LOGIC;
			 en3_o 		:	out  STD_LOGIC;
			 nd_o		: 	out	 STD_LOGIC;
			 addr0_o 	:	out  STD_LOGIC_VECTOR (DREGS_Ad_bits-1 downto 0);
			 addr1_o 	:	out  STD_LOGIC_VECTOR (DREGS_Ad_bits-1 downto 0);
			 addrq1_o 	:	out  STD_LOGIC_VECTOR (DREGS_Ad_bits-1 downto 0);
			 addrq2_o 	:	out  STD_LOGIC_VECTOR (DREGS_Ad_bits-1 downto 0)
			);
end BRdecoder;

architecture Behavioral of BRdecoder is
		--Selector expressions
		signal st_id_do : std_logic_vector(3+STRIPS_Ad_bits+TILES_Ad_bits downto 0);-- := ins_ctrl_i&ins_addr_i(5 downto 0)&done_i; --current state, reffered to strip ID, done signal
		signal st_id : std_logic_vector(3+STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0);-- := ins_ctrl_i&ins_addr_i(5 downto 0);  --current incoming STATE and refferenced strip address
		signal st_do : std_logic_vector(3 downto 0); --:= ins_ctrl_i&done_i;	--current state and done signal
		signal opcode_s : std_logic_vector(OPCODE_C-1 downto 0);
		signal instruction_is : std_logic_vector (INSTR_WIDTH_C-1 downto 0);
		signal switch : std_logic := '0';
		signal dontcare: std_logic_vector(STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0):=(others=> '-');

begin

	st_id_do <= ins_ctrl_i&ins_addr_i(STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0)&done_i;
	st_id <= ins_ctrl_i&ins_addr_i(STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0); 
	st_do <= ins_ctrl_i&done_i;
	opcode_s <= instruction_is (INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-1 downto INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C);--31->26
------------------------------

	en0_o <= '1' when std_match(st_id_do,"100"&Dstrip_ID&"-") else --OFF_LOAD local
			 '1' when std_match(st_id_do,"111"&dontcare&'0') else		--In RUN2, and not done, fetch data from mem
--			 '1' when std_match(st_id_do,"101"&"------"&'0') else		--In RUN3, and not done, fetch data from mem
		  	 '0';
		
	  addr0_o <= ins_addr_i(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) when std_match(st_id_do,"100"&Dstrip_ID&"-") else	--OFF_LOAD local
--						 instruction_is(DREGS_Ad_bits-1 downto 0) when std_match(st_id_do,"111"&"------"&'0') else		--In RUN2, not done, fetch data from mem
						 instruction_is(DREGS_Ad_bits-1 downto 0) when std_match(st_id_do,"111"&dontcare&'0') else		--In RUN2, not done, fetch data from mem
--						 instruction_is(DREGS_Ad_bits-1 downto 0) when std_match(st_id_do,"101"&"------"&'0') else		--In RUN3, not done, fetch data from mem
						 (others => '-');
------------------------------

		with st_do select
				en1_o <=
						 '1' when "111"&"0",	--In RUN2 and not done, fetching data for the execution phase.
--						 '1' when "101"&"0",	--In RUN3 and not done, fetching data for the execution phase.
						 '0' when others;	

		with st_do select
				addr1_o <= instruction_is(DREGS_Ad_bits+DREGS_Ad_bits-1 downto DREGS_Ad_bits) when "111"&"0",	--In RUN2, not done, fetch data from mem
--						   instruction_is(DREGS_Ad_bits+DREGS_Ad_bits-1 downto DREGS_Ad_bits) when "101"&"0",	--In RUN3, not done, fetch data from mem
						   (others => '-') when others;
------------------------------

		en2_o <= '1' when std_match(st_id,"010"&Dstrip_ID) else	--When 'my' turn to LOAD_DATA 
				 '0' when (ins_addr_i(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) = instruction_is(INSTR_WIDTH_C-1 downto INSTR_WIDTH_C-DREGS_Ad_bits)) else	--In execute state and done is high but addr2 ==addr3
				 '1' when std_match(st_do,"101"&"1") else --In execute state and done is high AND addr2 != addr3 
				 '0';

	   addrq1_o <= ins_addr_i(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) when std_match(st_id_do, "010"&Dstrip_ID&"-") else	--When 'my' turn to LOAD_DATA
--				   instruction_is(INSTR_WIDTH_C-1 downto INSTR_WIDTH_C-DREGS_Ad_bits) when std_match (st_id_do ,"101"&"------"&"1") else	--In RUN3 and done is high save result or data from another tile
				   instruction_is(INSTR_WIDTH_C-1 downto INSTR_WIDTH_C-DREGS_Ad_bits) when std_match (st_id_do ,"101"&dontcare&"1") else	--In RUN3 and done is high save result or data from another tile
				   (others => '-');
------------------------------

	   en3_o <=	'0' when (std_match(st_do,"101"&"1") and opcode_s = "000010")else --In execute state and saving result once done but opcode == NOP
				'0' when (std_match(st_do,"101"&"1") and opcode_s = "001000")else --In execute state and saving result once done but opcode == Branch
				'1' when (std_match(st_do,"101"&"1")) else
				'0';

--	   addrq2_o <= ins_addr_i(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) when std_match(st_id_do,"101"&"------"&"1") else --In RUN3 and done is high save result in same location as instruction came from - current execution row location
	   addrq2_o <= ins_addr_i(INS_ADDR_CD-1 downto INS_ADDR_CD-DREGS_Ad_bits) when std_match(st_id_do,"101"&dontcare&"1") else --In RUN3 and done is high save result in same location as instruction came from - current execution row location
						   (others => '-');

------------------------------

		with ins_ctrl_i select		
				CE_o <= '1' when "101",		--High only during execution and save stage of RUN
						'0' when others;
------------------------------

		off_load_o <= '0' when (st_id = "100"&Dstrip_ID) else --OFF_LOAD local
					  '1';
------------------------------

		opcode_o <= instruction_is (INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-1 downto INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C);--31->26
		sel0_o 	 <= instruction_is (INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C-STRIPS_Ad_bits-1 downto INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C-STRIPS_Ad_bits-STRIPS_Ad_bits); --22-20
		sel1_o	 <= instruction_is (INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C-1 downto INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits-OPCODE_C-STRIPS_Ad_bits); --25->23
		selq_o   <= instruction_is (INSTR_WIDTH_C-DREGS_Ad_bits-1 downto INSTR_WIDTH_C-DREGS_Ad_bits-TILES_Ad_bits); --34->32

		with ins_ctrl_i select
				nd_o <= switch when "101",
						'0' when others;
						
		process (clk)
		begin
				if rising_edge(clk) then
						instruction_is <= instruction_i;
				
						case ins_ctrl_i is
								when "101"=>
										switch <= '0';
								when others =>
										switch <= '1';
						end case;

				end if;

		end process;

end Behavioral;

