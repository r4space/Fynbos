----------------------------------------------------------------------------------
-- Create Date: 25/10/2010 
-- Project: Parameterised
-- Module Name: Data BRAM wrapper
-- Description: Wrapper for D_BRAM_gen, takes care of decoding when to enable which ports and switches incomming adress lines as appropriate
-- Revision: 0.01 - File Created
-- Additional Comments:
		-- The decoder sends address and control lines to the D_BRAM for 4 different ports, only 2 ports actually exist, this wrapper takes care of determing which address and control lines are switched to the actual ports when.
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;
use work.hydra_parameters.all;
---- Uncomment the following library declaration if instantiating
---- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;
entity data_bram_wrapper is

		Port ( addr0 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
           addr1 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
           addr2 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
           addr3 : in  std_logic_vector (DREGS_Ad_bits-1 downto 0);
           en0 : in  STD_LOGIC;
           en1 : in  STD_LOGIC;
           en2 : in  STD_LOGIC;
           en3 : in  STD_LOGIC;
           dout0 : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
           dout1  : out  std_logic_vector (DATA_SIZE_C-1 downto 0);
           din0 : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
           din1 : in  std_logic_vector (DATA_SIZE_C-1 downto 0);
   		   clk : in std_logic);

end data_bram_wrapper;

architecture rtl of data_bram_wrapper is
		
		signal addressA : std_logic_vector (DREGS_Ad_bits-1 downto 0) := (others => '-');
		signal addressB : std_logic_vector (DREGS_Ad_bits-1 downto 0) := (others => '-');
		signal data_inA : std_logic_vector (DATA_SIZE_C-1 downto 0) := (others => '-');
		signal data_inB : std_logic_vector (DATA_SIZE_C-1 downto 0) := (others => '-');
		signal data_outA : std_logic_vector(DATA_SIZE_C-1 downto 0) := (others => '-');
		signal data_outB : std_logic_vector (DATA_SIZE_C-1 downto 0) := (others => '-');
		signal enableA : std_logic := '0';
		signal enableB : std_logic := '0';
		signal we_A : std_logic := '0';
		signal we_B : std_logic := '0';
		
		component D_BRAM_YxZ 
				port (
						clka : IN std_logic;
						clkb : IN std_logic;
						ena : IN std_logic;
						enb : IN std_logic;
						wea : in std_logic;
						web : in std_logic;
						addra : IN std_logic_vector(DREGS_Ad_bits-1 downto 0);
						addrb : IN std_logic_vector(DREGS_Ad_bits-1 downto 0);
						dia : IN std_logic_vector(DATA_SIZE_C-1 downto 0);
						dib : IN std_logic_vector(DATA_SIZE_C-1 downto 0);
						doa : OUT std_logic_vector(DATA_SIZE_C-1 downto 0);
						dob : OUT std_logic_vector(DATA_SIZE_C-1 downto 0)
					);
			end component D_BRAM_YxZ;
			
begin
			data: D_BRAM_YxZ
				port map (
							clka => clk,
							clkb => clk,
							ena => enableA,
							enb => enableB,
							wea => we_A,
							web => we_B,
							addra => addressA, 
							addrb => addressB,
							dia => data_inA,
							dib => data_inB,
							doa => data_outA,
							dob => data_outB
						 );
				
--Port A has been assigned addr0 and addr2, i.e it will be reading addr0 and writing to addr2
-- Therefore portA is enabled when either en0 or en2 are high				

				addressA <= addr0 when (en0 = '1' and en2 = '0') else
							addr2 when (en0 = '0' and en2 = '1') else
							(others=> '0');
				enableA <= '1' when (en0 = '1' xor en2 = '1') else
						   '0';
				
--Port B has been assigned addr1 and addr3, i.e it will be reading addr1 and writing to addr3
-- Therefore portB is enabled when either en1 or en3 are high				

				addressB <= addr1 when (en1 = '1' and en3 = '0') else
							addr3 when (en1 = '0' and en3 = '1') else
							(others => '0');
				enableB <= '1' when (en1 = '1' xor en3 = '1') else
						   '0';
				
--PortA is only write enabled when data is being stored at addr2 and therefore when en2 is high.
--Similarily, portB is only write enabled when data is being stored at addr3 and therefore when en3 is high.
				we_A <= en2;			
				we_B <= en3;
--				we_A(0) <= en2;			
--				we_B(0) <= en3;
				
--dinta is allways connected to din0 via data_inA				
--dintb is allways connected to din1 via data_inB
				data_inA <= din0;
				data_inB <= din1;
				
--douta is allways connected to dout0 via data_outA
--doutb is allways connected to dout1 via data_outB				
				dout0 <= data_outA;
				dout1 <= data_outB;
				
end rtl;
