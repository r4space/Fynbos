---------------------------------------------------------------------------------
-- ROACH 10Gbe framework
-- For useage info view: http://casper.berkeley.edu/wiki/Ten_GbE_v2
-- David Macleod 15/12/2010
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

entity top_level is
		Port (sys_clk_n : in STD_LOGIC;
				sys_clk_p : in STD_LOGIC;
				dly_clk_n : in STD_LOGIC;
				dly_clk_p : in STD_LOGIC;
				aux0_clk_n  : in STD_LOGIC;
				aux0_clk_p  : in STD_LOGIC;
				aux1_clk_n  : in STD_LOGIC;
				aux1_clk_p  : in STD_LOGIC;
				epb_clk_in  : in STD_LOGIC;
				epb_data : inout STD_LOGIC_VECTOR(15 downto 0);
				epb_addr : in STD_LOGIC_VECTOR(22 downto 0);
				epb_addr_gp : in STD_LOGIC_VECTOR(5 downto 0);
				epb_cs_n : in STD_LOGIC;
				epb_be_n : in STD_LOGIC_VECTOR(1 downto 0);
				epb_r_w_n : in STD_LOGIC;
				epb_oe_n : in STD_LOGIC;
				epb_rdy : out STD_LOGIC;
				ppc_irq_n : out STD_LOGIC;
				mgt_ref_clk_top_n : in STD_LOGIC;
				mgt_ref_clk_top_p : in STD_LOGIC;
				mgt_ref_clk_bottom_n : in STD_LOGIC;
				mgt_ref_clk_bottom_p : in STD_LOGIC;
				mgt_rx_top_1_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_1_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_1_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_1_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_0_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_0_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_0_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_0_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_1_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_1_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_1_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_1_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_0_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_0_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_0_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_0_p : out STD_LOGIC_VECTOR(3 downto 0)
				);
end top_level;

architecture Behavioral of top_level is

component system is
    Port ( 	--ROACH Ports, to the edge of the FPGA
				sys_clk_n : in STD_LOGIC;
				sys_clk_p : in STD_LOGIC;
				dly_clk_n : in STD_LOGIC;
				dly_clk_p : in STD_LOGIC;
				aux0_clk_n  : in STD_LOGIC;
				aux0_clk_p  : in STD_LOGIC;
				aux1_clk_n  : in STD_LOGIC;
				aux1_clk_p  : in STD_LOGIC;
				epb_clk_in  : in STD_LOGIC;
				epb_data : inout STD_LOGIC_VECTOR(15 downto 0);
				epb_addr : in STD_LOGIC_VECTOR(22 downto 0);
				epb_addr_gp : in STD_LOGIC_VECTOR(5 downto 0);
				epb_cs_n : in STD_LOGIC;
				epb_be_n : in STD_LOGIC_VECTOR(1 downto 0);
				epb_r_w_n : in STD_LOGIC;
				epb_oe_n : in STD_LOGIC;
				epb_rdy : out STD_LOGIC;
				ppc_irq_n : out STD_LOGIC;
				mgt_ref_clk_top_n : in STD_LOGIC;
				mgt_ref_clk_top_p : in STD_LOGIC;
				mgt_ref_clk_bottom_n : in STD_LOGIC;
				mgt_ref_clk_bottom_p : in STD_LOGIC;
				mgt_rx_top_1_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_1_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_1_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_1_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_0_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_top_0_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_0_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_top_0_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_1_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_1_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_1_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_1_p : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_0_n : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_rx_bottom_0_p : in STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_0_n : out STD_LOGIC_VECTOR(3 downto 0);
				mgt_tx_bottom_0_p : out STD_LOGIC_VECTOR(3 downto 0);
				-- 10Gbe and other ports, internal, brought out for your use		
				newtop_gbe0_tx_valid_pin : in STD_LOGIC;
				newtop_rst_user_data_out_pin : out STD_LOGIC_VECTOR(31 downto 0);
				newtop_gbe0_rx_ack_pin : in STD_LOGIC;
				newtop_gbe0_tx_end_of_frame_pin : in STD_LOGIC;
				newtop_gbe0_tx_afull_pin : out STD_LOGIC;
				newtop_gbe0_tx_overflow_pin : out STD_LOGIC;
				newtop_gbe0_tx_data_pin : in STD_LOGIC_VECTOR(63 downto 0);
				newtop_gbe0_rx_valid_pin : out STD_LOGIC;
				newtop_gbe0_rx_end_of_frame_pin : out STD_LOGIC;
				newtop_gbe0_rx_data_pin : out STD_LOGIC_VECTOR(63 downto 0);
				newtop_gbe0_rx_source_ip_pin : out STD_LOGIC_VECTOR(31 downto 0);
				newtop_gbe0_rx_source_port_pin : out STD_LOGIC_VECTOR(15 downto 0);
				newtop_gbe0_rx_bad_frame_pin : out STD_LOGIC;
				newtop_gbe0_rx_overrun_pin : out STD_LOGIC; -- Already tied to overrun_ack in the net list
				-- User clock, internal, for your use
				sys_clk_pin : out STD_LOGIC;
				status_r_pin : in std_logic_vector (31 downto 0);
				sys_reset_o_pin : out std_logic
				);
end component system;

signal gbe0_tx_data, gbe0_rx_data : STD_LOGIC_VECTOR(63 downto 0);
signal sys_clk, gbe0_rx_valid, gbe0_rx_end_of_frame, gbe0_rx_bad_frame, gbe0_tx_valid, gbe0_tx_end_of_frame,gbe0_tx_afull, gbe0_tx_overflow, gbe0_rx_overrun, gbe0_rx_ack : STD_LOGIC;
signal gbe0_rx_source_ip, gbe0_tx_dest_ip : STD_LOGIC_VECTOR(31 downto 0);
signal gbe0_rx_source_port, gbe0_tx_dest_port : STD_LOGIC_VECTOR(15 downto 0);

signal rst_s : std_logic_vector(31 downto 0);
signal rst_ss : std_logic; --Purley a place holder, I'm not quite sure what the sys_reset_o_pin relates to so just ignoreing the output with this signal
signal status_s : std_logic_vector(31 downto 0);

component system_top is
  port (
   		clk 			: in  std_logic;
    	reset 			: in  std_logic;
  		status			: out std_logic_vector (3 downto 0);
		
		sim_rx_data			: in std_logic_vector (63 downto 0);
  		sim_rx_valid		: in std_logic;
		sim_rx_ack			: out std_logic;


  		sim_tx_data			: out std_logic_vector(63 downto 0);
		sim_tx_valid		: out std_logic;
		sim_tx_end_of_frame : out std_logic
		);
end component system_top;

begin
tenEth : component system
    port map (	--ROACH Ports, to the edge of the FPGA
					sys_clk_n => sys_clk_n,
					sys_clk_p => sys_clk_p,
					dly_clk_n => dly_clk_n,
					dly_clk_p => dly_clk_p,
					aux0_clk_n => aux0_clk_n,
					aux0_clk_p => aux0_clk_p,
					aux1_clk_n => aux1_clk_n,
					aux1_clk_p => aux1_clk_p,
					epb_clk_in => epb_clk_in,
					epb_data => epb_data,
					epb_addr => epb_addr,
					epb_addr_gp => epb_addr_gp,
					epb_cs_n => epb_cs_n,
					epb_be_n => epb_be_n,
					epb_r_w_n => epb_r_w_n,
					epb_oe_n => epb_oe_n,
					epb_rdy => epb_rdy,
					ppc_irq_n => ppc_irq_n,
					mgt_ref_clk_top_n => mgt_ref_clk_top_n,
					mgt_ref_clk_top_p => mgt_ref_clk_top_p,
					mgt_ref_clk_bottom_n => mgt_ref_clk_bottom_n,
					mgt_ref_clk_bottom_p => mgt_ref_clk_bottom_p,
					mgt_rx_top_1_n => mgt_rx_top_1_n,
					mgt_rx_top_1_p => mgt_rx_top_1_p,
					mgt_tx_top_1_n => mgt_tx_top_1_n,
					mgt_tx_top_1_p => mgt_tx_top_1_p,
					mgt_rx_top_0_n => mgt_rx_top_0_n,
					mgt_rx_top_0_p => mgt_rx_top_0_p,
					mgt_tx_top_0_n => mgt_tx_top_0_n,
					mgt_tx_top_0_p => mgt_tx_top_0_p,
					mgt_rx_bottom_1_n => mgt_rx_bottom_1_n,
					mgt_rx_bottom_1_p => mgt_rx_bottom_1_p,
					mgt_tx_bottom_1_n => mgt_tx_bottom_1_n,
					mgt_tx_bottom_1_p => mgt_tx_bottom_1_p,
					mgt_rx_bottom_0_n => mgt_rx_bottom_0_n,
					mgt_rx_bottom_0_p => mgt_rx_bottom_0_p,
					mgt_tx_bottom_0_n => mgt_tx_bottom_0_n,
					mgt_tx_bottom_0_p => mgt_tx_bottom_0_p,
					-- 10Gbe ports, internal, for your use					
					newtop_gbe0_tx_valid_pin => gbe0_tx_valid,
					newtop_gbe0_tx_afull_pin => gbe0_tx_afull,
					newtop_gbe0_tx_overflow_pin => gbe0_tx_overflow,
					newtop_gbe0_tx_end_of_frame_pin => gbe0_tx_end_of_frame,
					
					newtop_gbe0_tx_data_pin => gbe0_tx_data,
					--The following bit swap makes it possible to read the returned data back in bytes not characters catering for the reverse-bit-order the network sends the data in
--					newtop_gbe0_tx_data_pin(7 downto 0) => gbe0_tx_data(63 downto 56),
--					newtop_gbe0_tx_data_pin(15 downto 8) => gbe0_tx_data(55 downto 48),
--					newtop_gbe0_tx_data_pin(23 downto 16) => gbe0_tx_data(47 downto 40),
--					newtop_gbe0_tx_data_pin(31 downto 24) => gbe0_tx_data(39 downto 32),
--					newtop_gbe0_tx_data_pin(39 downto 32) => gbe0_tx_data(31 downto 24),
--					newtop_gbe0_tx_data_pin(47 downto 40) => gbe0_tx_data(23 downto 16),
--					newtop_gbe0_tx_data_pin(55 downto 48) => gbe0_tx_data(15 downto 8),
--					newtop_gbe0_tx_data_pin(63 downto 56) => gbe0_tx_data(7 downto 0),

					newtop_gbe0_rx_valid_pin => gbe0_rx_valid,
					newtop_gbe0_rx_end_of_frame_pin => gbe0_rx_end_of_frame,
					newtop_gbe0_rx_data_pin => gbe0_rx_data,
					newtop_gbe0_rx_source_ip_pin => gbe0_rx_source_ip,
					newtop_gbe0_rx_source_port_pin => gbe0_rx_source_port,
					newtop_gbe0_rx_bad_frame_pin => gbe0_rx_bad_frame,
					newtop_gbe0_rx_overrun_pin => gbe0_rx_overrun, -- Already tied to overrun_ack in the net list
					newtop_gbe0_rx_ack_pin => gbe0_rx_ack,	
					-- User clock, internal, for your use
					sys_clk_pin => sys_clk,
					status_r_pin => status_s,
					newtop_rst_user_data_out_pin => rst_s
					);	

	hydra_system_top: system_top
	port map (
	    	clk => sys_clk, 		
	    	reset => rst_s(0),
	  		status => status_s(3 downto 0),
	
			sim_rx_data =>	gbe0_rx_data,
	  		sim_rx_valid => gbe0_rx_valid,
			sim_rx_ack => gbe0_rx_ack,

	  		sim_tx_data => gbe0_tx_data,
			sim_tx_valid => gbe0_tx_valid,
			sim_tx_end_of_frame => gbe0_tx_end_of_frame
			);
	--RX: Bad Frame : OVERRUN : EOF : ACK 
	--TX: EOF : AFULL : OVERFLOW : VALID
	status_s(11 downto 4) <= gbe0_rx_bad_frame&gbe0_rx_overrun&gbe0_rx_end_of_frame&gbe0_rx_ack&gbe0_tx_end_of_frame&gbe0_tx_afull&gbe0_tx_overflow&gbe0_tx_valid;
end Behavioral;

