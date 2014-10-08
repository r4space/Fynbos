library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.EXT;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use IEEE.numeric_std.all;
use work.hydra_parameters.all;
library UNISIM;  
use UNISIM.Vcomponents.all;
entity instr_bram_wrapper is
		generic (Dstrip_ID : std_logic_vector ((STRIPS_Ad_bits +TILES_Ad_bits-1) downto 0));--:= "000000");
		 Port ( ins_addr_ID   : in  std_logic_vector (INS_ADDR_CI-1 downto 0);
		        clk          : in  STD_LOGIC;
		   		ins_ctrl		: in std_logic_vector (2 downto 0);
		   		ins_data		: in std_logic_vector (DATA_SIZE_C-1 downto 0);
           		dout         : out std_logic_vector (INSTR_WIDTH_C-1 downto 0)
          		);
end instr_bram_wrapper;

architecture rtl of instr_bram_wrapper is
		
		component I_BRAM is
				port(clka    : in std_logic;
				      ena    : in std_logic;
    			      wea    : in std_logic;
    			      addra  : in std_logic_vector(IREGS_Ad_bits-1 downto 0);
    			      dia    : in std_logic_vector(INSTR_WIDTH_C-1 downto 0);
    			      doa    : out std_logic_vector(INSTR_WIDTH_C-1 downto 0)
  					);
		end component;

		signal wens, ens : std_logic := '0';
		signal instruction_s : std_logic_vector(INSTR_WIDTH_C-1 downto 0) := (others => '0');
		signal address_s : std_logic_vector(IREGS_Ad_bits-1 downto 0);
	

begin


	instr_bram: I_BRAM 
				port map (
					 	clka => clk,
				      	ena  => ens,
    					wea  => wens,  
    			      	addra => address_s, 
    			      	dia => instruction_s,
    			      	doa => dout
  						);

				process (clk)
				begin
						if rising_edge(clk) then

								address_s <= ins_addr_ID(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits);

								case ins_ctrl is
										when "001" => --1st word
												
												ens <= '0';
												wens <= '0';
												instruction_s(INSTR_WIDTH_C-1 downto INSTR_WIDTH_C-DATA_SIZE_C) <= ins_data;

										when "011" => --2nd word
												if Dstrip_ID = ins_addr_ID((STRIPS_Ad_bits+TILES_Ad_bits-1) downto 0) then
														wens <= '1';
														ens <= '1';
												else 
														wens <= '0';
														ens <= '0';
												end if;

												instruction_s(INSTR_WIDTH_C-DATA_SIZE_C-1 downto 0) <= ins_data(INSTR_WIDTH_C-DATA_SIZE_C-1 downto 0);

										when"110" => --Fetch instruction

												ens <= '1';
												wens <= '0';

										when others =>
												ens <= '0';
												wens <= '0';
								end case;
						end if;
				end process;


end rtl;
