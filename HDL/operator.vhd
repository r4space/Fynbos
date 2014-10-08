----------------------------------------------------------------------------------
-- Create Date: 27/10/2010 
-- Project: Parameterised
-- Module Name: Operator
-- Description: Strip ALU
-- Revision: 0.01 - File Created
-- Additional Comments:
--Current number format: fixed-point is : 20:16
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
--use IEEE.STD_LOGIC_ARITH.all;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
--use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;
-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity operator is
		 port ( a : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        b : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
		        opcode : in  std_logic_vector (OPCODE_C-1 downto 0);
		        clk : in  STD_LOGIC;
		        ce : in  STD_LOGIC;
		 		nd : in STD_LOGIC;
		        done : out  std_logic_vector(1 downto 0);
		        c : out std_logic_vector (DATA_SIZE_C-1 downto 0)
				);
end operator;

architecture Behavioral of operator is

--		signal OOB_s : std_logic:= '0';
		signal tog : std_logic := '0';
		
		--ADD/SUB signals
		signal ASU_OOB_s : std_logic:= '0';
		signal ASO_OOB_s : std_logic:= '0';
		signal operation_s : std_logic_vector(5 downto 0) := "000000";
        signal AS_c : std_logic_vector ( DATA_SIZE_C-1 downto 0) := (others => '0');
		signal AS_nd_s : std_logic := '0';
		signal AS_rdy : std_logic := '0';

		--MUL signals
		signal MU_OOB_s : std_logic:= '0';
		signal MO_OOB_s : std_logic:= '0';
		signal MUL_rdy : std_logic := '0';
        signal MUL_c : std_logic_vector ( DATA_SIZE_C-1 downto 0) := (others => '0');
		signal M_nd_s : std_logic := '0';

--		--DIV signals
--		signal DU_OOB_s : std_logic:= '0';
--		signal DO_OOB_s : std_logic:= '0';
--		signal DIV_rdy : std_logic := '0';
--	  	signal DIV_c : std_logic_vector ( DATA_SIZE_C-1 downto 0) := (others => '0');
--		signal D_nd_s : std_logic := '0';
		
		--Compare signals
   		signal CP_c : std_logic_vector(0 downto 0) := (others => '0');
		signal CP_nd_s : std_logic := '0';
--		signal CP_rdy : std_logic := '0';


		component float_add_sub
			port (
			a: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			b: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			operation: in std_logic_vector(5 downto 0);
			operation_nd: in std_logic;
			clk: in std_logic;
			result: out std_logic_vector(DATA_SIZE_C-1 downto 0);
			underflow: out std_logic;
			overflow: out std_logic;
			rdy: out std_logic
			);
		end component;

		component float_mul
			port (
			a: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			b: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			operation_nd: in std_logic;
			clk: in std_logic;
			result: out std_logic_vector(DATA_SIZE_C-1 downto 0);
			underflow: out std_logic;
			overflow: out std_logic;
			rdy: out std_logic
			);
		end component;
		
--		component float_div
--			port (
--			a: in std_logic_vector(DATA_SIZE_C-1 downto 0);
--			b: in std_logic_vector(DATA_SIZE_C-1 downto 0);
--			operation_nd: in std_logic;
--			clk: in std_logic;
--			result: out std_logic_vector(DATA_SIZE_C-1 downto 0);
--			underflow: out std_logic;
--			overflow: out std_logic;
--			rdy: out std_logic
--			);
--		end component;

		component float_compare
			port (
			a: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			b: in std_logic_vector(DATA_SIZE_C-1 downto 0);
			operation: in std_logic_vector(5 downto 0);
			operation_nd: in std_logic;
--			clk: in std_logic;
			result: out std_logic_vector(0 downto 0)
--			rdy : out std_logic
			);
		end component;

begin

		addsub : float_add_sub
				port map (
					a => a,
					b => b,
					operation => opcode,
					operation_nd => AS_nd_s,
					clk => clk,
					result => AS_c,
					underflow => ASU_OOB_s,
					overflow => ASO_OOB_s,
					rdy => AS_rdy
					);

		mul : float_mul
				port map (
					a => a,
					b => b,
					operation_nd => M_nd_s,
					clk => clk,
					result => MUL_c,
					underflow => MU_OOB_s,
					overflow => MO_OOB_s,
					rdy => MUL_rdy
					);
		  	
--		div : float_div
--				port map (
--					a => a,
--					b => b,
--					operation_nd => D_nd_s,
--					clk => clk,
--					result => DIV_c,
--					underflow => DU_OOB_s,
--					overflow => DO_OOB_s,
--					rdy => DIV_rdy
--					);
				
		comp : float_compare
				port map (
					a => a,
					b => b,
					operation => operation_s,
					operation_nd => CP_nd_S,
--					clk => clk,
					result => CP_c
--					rdy => CP_rdy
				);

				with opcode select
						AS_nd_s <= nd when "000000" | "000001",
								   '0' when others;
				with opcode select
						M_nd_s <= nd when "000011",
								  '0' when others;
--				with opcode select
--						D_nd_s <= nd when "000100",
--								  '0' when others;

				with opcode select
						CP_nd_s <= nd when "001100"|"010100"|"100100"|"000110"|"000111"|"101100"|"011100"|"110100", --// NE, LTE, GTE
								   '0' when others;
				with opcode select
						operation_s <= "001100" when "000110"|"000111",
									   opcode when others;

		process(clk)

			begin

				if rising_edge(clk) then

--						OOB_s <= '0';
						done(1) <= '0';
--						done(0) <= OOB_s;
						done(0) <= '0';
						c <= (others => '-'); 
						tog <= '0';
	
						if ce = '1' then
								tog <= '0';

								case opcode is
										when "000000"|"000001" => 	--ADD/SUB
												c <= AS_c;
--												OOB_s <= ASU_OOB_s or ASO_OOB_s;
												done(0)<= ASU_OOB_s or ASO_OOB_s;
												if AS_rdy = '1' then
														done(1) <= '1';
														tog <= '1';
												elsif tog = '1' then
														done(1) <= '1';
														tog <= '1';
												else
														done(1) <= '0';
														tog <= '0';
												end if;
--												done(1) <= AS_rdy;

										when "000010" =>	--NOP
												done(1) <= '1';	--If no opcode or data was provided but the clock was enabled as the rest of hydra is working a done still needs to be returned to allow the next instruction to be issued
--												OOB_s <= '0';
												done(0) <= '0';
												c <= (others => '-');

										when "000011" =>	-- MUL
												
												c <= MUL_c;
--												OOB_s <= MU_OOB_s or MO_OOB_s;
												done(0) <= MU_OOB_s or MO_OOB_s;
												if MUL_rdy = '1' then
														done(1) <= '1';
														tog <= '1';
												elsif tog = '1' then
														done(1) <= '1';
														tog <= '1';
												else
														done(1) <= '0';
														tog <= '0';
												end if;
--												done(1) <= MUL_rdy;

										when "000101" =>	--Copy
												c <= a;
												done(1) <= '1';
--												OOB_s<= '0';
												done(0) <= '0';

										when "000110" =>	--MAX
												
												if CP_c = "1" then --TRUE
														c <= b;
												else
														c<= a;
												end if;

--												done(1) <= CP_rdy;
												done(1) <='1'; 
--												OOB_s<= '0';
												done(0) <= '0';


										when "000111"=>	--MIN

												if CP_c = "1" then --TRUE
														c <= a;
												else
														c<= b;
												end if;

--												done(1) <= CP_rdy;
												done(1) <= '1';
--												OOB_s<= '0';
												done(0) <= '0';
		
										when "001100"|"010100"|"100100" |"101100"|"011100"|"110100" =>	--Less than| equal to | Greater Than
											
											c(DATA_SIZE_C-1 downto 1) <= (others => '0');
											c(0 downto 0) <= CP_c(0 downto 0);

--											done(1) <= CP_rdy;
											done(1) <= '1';
--											OOB_s<= '0';
											done(0) <= '0';

										when others =>
	
												done(1) <= '1';
--												OOB_s <= '0';
												done(0) <= '0';
												c <= (others => '-');
								end case;
						else

  								done(1) <= '0';
--  								OOB_s <= '0';
								done(0) <= '0';
								c <= (others => '-');
								tog <= '0';
		
						end if; --End CE
				end if; --end rising edge
		end process;

end Behavioral;

