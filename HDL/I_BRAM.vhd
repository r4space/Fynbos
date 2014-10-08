----------------------------------------------------------------------------------
-- Create Date: 25/10/2010 
-- Project: Parameterised
-- Module Name: Data BRAM
-- Description: This forms the instruction memory a copy of which will be in each strip ('core')
-- Revision: 0.01 - File Created
-- Additional Comments:
					--The original configuration was for 36bitsx1024words BRAM , this is now parameterised however.
					--Dual port: Dual read and write
					--Buffered data outputs (to gain speed), buffering the input sdidn't appear to improve speed at all
					--No change mode
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.hydra_parameters.all;
library UNISIM;  
use UNISIM.Vcomponents.all;
entity I_BRAM is
    port(clka    : in std_logic;
          ena    : in std_logic;
          wea    : in std_logic;
          addra  : in std_logic_vector(IREGS_Ad_bits-1 downto 0);
          dia    : in std_logic_vector(INSTR_WIDTH_C-1 downto 0);
          doa    : out std_logic_vector(INSTR_WIDTH_C-1 downto 0)
  		);

	attribute ram_style: string;
	attribute ram_style of I_BRAM: entity is "block";	


end I_BRAM;

architecture Behavioral of I_BRAM is
	
	type RAM_TYPE is array (((2**IREGS_Ad_bits)-1) downto 0) of std_logic_vector(INSTR_WIDTH_C-1 downto 0);	--Depth by width
	signal RAM: RAM_TYPE := (others=> (others=>'0'));

	signal doa_s : std_logic_vector (INSTR_WIDTH_C-1 downto 0) := (others => '0'); 

begin

    process (clka)
    begin

		if rising_edge(clka) then

		  doa <= doa_s;	

          if ena = '1' then
              if wea = '1' then
                  RAM(conv_integer(addra)) <= dia;
			  else
	              doa_s <= RAM(conv_integer(addra));

              end if;
          end if;

        end if;
    end process;
end Behavioral;

