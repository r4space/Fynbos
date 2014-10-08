----------------------------------------------------------------------------------
-- Create Date: 25/10/2010 
-- Project: Parameterised
-- Module Name: Data BRAM
-- Description: This forms the data memory a copy of which will be in each strip ('core')
-- Revision: 0.01 - File Created
-- Additional Comments:
					--The original configuration was for 32bitsx512words BRAM , this is now parameterised however.
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

entity D_BRAM_YxZ is
    port(clka    : in std_logic;
          clkb   : in std_logic;
          ena    : in std_logic;	--Enables
          enb    : in std_logic;
          wea    : in std_logic;	--Write enables
          web    : in std_logic;
          addra  : in std_logic_vector(DREGS_Ad_bits-1 downto 0);	--A port address lines
          addrb  : in std_logic_vector(DREGS_Ad_bits-1 downto 0);
          dia    : in std_logic_vector(DATA_SIZE_C-1 downto 0);--A port data in
          dib    : in std_logic_vector(DATA_SIZE_C-1 downto 0);
          doa    : out std_logic_vector(DATA_SIZE_C-1 downto 0);	--A port data out
          dob    : out std_logic_vector(DATA_SIZE_C-1 downto 0)
  		);

	attribute ram_style: string;
	attribute ram_style of D_BRAM_YxZ: entity is "block";	

--	attribute ram_extract: string;
--	attribute ram_extract of BRAM_32x512: entity is "yes"; 	--Don't use logic to make more BRAM if you're running out of BRAM's

end D_BRAM_YxZ;

architecture Behavioral of D_BRAM_YxZ is
  attribute buffer_type: string;
--	type RAM_TYPE is array (((2**10)-1) downto 0) of std_logic_vector(DATA_SIZE_C-1 downto 0);	--Depth by width
	type RAM_TYPE is array (((2**DREGS_Ad_bits)-1) downto 0) of std_logic_vector(DATA_SIZE_C-1 downto 0);	--Depth by width
    shared variable RAM : RAM_TYPE := (others=>(others=>'0'));

	signal doa_s : std_logic_vector(DATA_SIZE_C-1 downto 0) := (others => '0');
	signal dob_s : std_logic_vector(DATA_SIZE_C-1 downto 0) := (others=> '0');

begin

    process (clka)
    begin
			if rising_edge(clka) then
			  doa <= doa_s;
              if ena = '1' then
                  if wea = '1' then
                      RAM(conv_integer(addra)) := dia;
				  else
	                  doa_s <= RAM(conv_integer(addra));
                  end if;
              end if;
        end if;
    end process;

    process (clkb)
    begin
			if rising_edge(clkb) then
	  		  dob <= dob_s;
              if enb ='1' then
                  if web = '1' then
                      RAM(conv_integer(addrb)) := dib;
				  else
    	              dob_s <= RAM(conv_integer(addrb));
                  end if;
         end if;
    end if;
    end process;

end Behavioral;

