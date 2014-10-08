library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_UNSIGNED.all;
use IEEE.STD_LOGIC_ARITH.all;
use IEEE.NUMERIC_STD.ALL;
use work.hydra_parameters.all;
---- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity new_ICON is
  port (
    	clk 				: in  std_logic;
    	reset_i				: in  std_logic;
  		status_o			: out std_logic_vector (3 downto 0);	--RESET: 0, COMMAND: 1, LI1:2, LI2:3, LD:4 RUN1:5, RUN2:6, RUN3:7, OF:8, ERROR:9
    	
		rx_data_i			: in std_logic_vector (63 downto 0);
  		rx_valid_i			: in std_logic;
		rx_ack_o			: out std_logic;

  		tx_data_o			: out std_logic_vector(63 downto 0);
		tx_valid_o			: out std_logic;
		tx_end_of_frame_o 	: out std_logic;

		ins_ctrl_o			: out std_logic_vector (2 downto 0);	
		ins_data_o			: out std_logic_vector (DATA_SIZE_C-1 downto 0);
		ins_addr_o			: out std_logic_vector (INS_ADDR_C - 1 downto 0);
		ins_done_i			: in std_logic_vector(1 downto 0);

		CPO_ctrl_i			: in std_logic;
		CPO_data_i			: in std_logic_vector(DATA_SIZE_C-1 downto 0);
		
		branch_cont_i		: in std_logic;
		branch_data_i		: in std_logic_vector (IREGS_Ad_bits-1 downto 0);
		dataCy_i			: in std_logic_vector (DATA_SIZE_C-1 downto 0)
		);
end entity new_ICON;


architecture behavioural of new_ICON is

		signal state : main_states; 
		signal txrx_st : TxRx_states;
------------------------------------------------------------------------------
		--Go back and remove all the 'default' assignments and see what happens 
		--See what the best encoding is again
------------------------------------------------------------------------------


--		attribute FSM_ENCODING : string;
--		attribute FSM_ENCODING of state : signal is "speed1";
--		attribute FSM_ENCODING of next_state : signal is "speed1";



		--Intenal: MAIN_STATE_PROCESS
		signal hold_addr_s 		: std_logic_vector (INS_ADDR_C-1 downto 0)	:= (others => '0');
		signal count_s 			: std_logic_vector (SC_LEN-INS_ADDR_C-3-1 downto 0)	:= (others => '0');
		signal numregs_s		: integer range 2048 downto 0 				:= NO_DREGS_C;
		signal endreg_s			: std_logic_vector (IREGS_Ad_bits-1 downto 0):= (others => '0');
		signal delay_s			: integer range 8 downto 0					:= 8;
		signal flcount_s		: std_logic_vector(2 downto 0)				:= "000";
		signal tog				: std_logic := '0';

		signal tx_data_s		: std_logic_vector(63 downto 0)	:= (others => '0');

		--Internal: TXRX_ST_PROCESS
		signal TXWcounter_s			: integer range 3 downto 0		:= 0;
		signal TXFULL_counter_s		: std_logic_vector(9 downto 0) := (others => '0');
--		signal wait_s : std_logic_vector(7 downto 0) := (others => '0');
		signal wait_s : std_logic_vector(19 downto 0) := (others => '0');

		--Constants
		constant filler 		: std_logic_vector(63 downto 0) 	:= (others => '0');	--Zeros for filling up concatinated signals
		constant ZERO_ADDRESS 	: std_logic_vector(INS_ADDR_C-1 downto 0) 	:= (others => '0');
		constant TXFULL			: std_logic_vector(9 downto 0) := "1111110001"; --1009

begin

--		temp_debug <= "000"&count_s;
--		with state select
--		temp_state <= "0001" when IDL,
--					  "0010" when CMD,
--					  "0011" when LD,
--					  "0100" when LD_FM,
--					  "0101" when LI1,
--					  "0110" when LI2,
--					  "0111" when LI_FM,
--					  "1000" when RUN1,
--					  "1001" when RUN2,
--					  "1010" when RUN3,
--					  "1011" when OFLD,
--					  "1100" when OFLDFLUSH,
--					  "1101" when FLUSH_O,	
--					  "1111" when others; --Includes reset cause it's not a state
--
--		with txrx_st select
--		temp_txrx_st <=   "0001" when idle,
--					 	  "0010" when WMR,
--						  "0011" when PMR,
--					 	  "0100" when CPKT,
--					 	  "0101" when POFLD,
--						  "0110" when BTPKT,
--					 	  "0111" when TPKT,
--						  "1000" when others;

MAIN_STATE_PROCESS:
		process (clk, reset_i)
		begin
			if rising_edge(clk) then
					if reset_i = '1' then

							state <= IDL;

							--Outputs
							status_o	<= "1110";	
							rx_ack_o 	<= '0';
							ins_ctrl_o	<= "000";
							ins_data_o	<= (others =>'0');
							ins_addr_o	<= (others =>'0');

							--Signals
							hold_addr_s <= (others =>'0');
							count_s		<= (others =>'0');
							numregs_s	<= 0;
							endreg_s	<= (others =>'0');
							delay_s		<= 0;
							flcount_s   <= "000";
							tog <= '0';
							tx_data_s	<= (others =>'0');
							                    
					else

							case (state) is

									when IDL =>

											--Outputs
											status_o	<= "0001";
											rx_ack_o	<= '1';
											ins_ctrl_o	<= "000";
											ins_data_o	<= (others => '0');
											ins_addr_o	<= (others => '0');
--
--											--Signals
											hold_addr_s <= (others =>'0');
											count_s		<= (others =>'0');
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											tog			<= '0';
											flcount_s	<= "000";
											tx_data_s	<= X"000000000000000E";
				
											if rx_valid_i = '1' then
													state <= CMD;
											else
													state <= IDL;
											end if;
			
									when CMD =>
											
											--Outputs
											status_o	<= "0010";
											ins_ctrl_o	<= "000";
											ins_data_o	<= (others => '0');
											ins_addr_o	<= (others => '0');

											--Signals
											delay_s		<= 7;
											tog <= '0';
											flcount_s	<= "000";
											tx_data_s	<= tx_data_s;
  										
											if rx_data_i(2 downto 0) = "001" then --LI
			
													hold_addr_s(INS_ADDR_CI-1 downto 0) <=rx_data_i(INS_ADDR_CI+2 downto 3);
													count_s(SC_LEN-INS_ADDR_CI-3-1 downto 0) <=rx_data_i(SC_LEN-1 downto INS_ADDR_CI+3);
													numregs_s<= 0;
													endreg_s <= (others =>'0');
													rx_ack_o <= '0';
	
													if rx_valid_i = '1' then
															state <= LI1;
													else
															state <= LI_FM;
													end if;
			
  										    elsif rx_data_i(2 downto 0) = "010" then --LD
  												
													rx_ack_o <= rx_valid_i;
  													hold_addr_s(INS_ADDR_CD-1 downto 0) <=rx_data_i(INS_ADDR_CD+2 downto 3);	--Start address
  													count_s(SC_LEN-INS_ADDR_CD-3-1 downto 0) <=rx_data_i(SC_LEN-1 downto INS_ADDR_CD+3);--Words to count 15:0 <= 35:20
  													numregs_s <= NO_DREGS_C;
													endreg_s <= (others =>'0');

													if rx_valid_i = '1' then
															state <= LOAD_DATA;
													else
															state <= LD_FM;
													end if;
  		
											elsif rx_data_i(2 downto 0) = "011" then --RUN 
			
													rx_ack_o <= '0';
													hold_addr_s(INS_ADDR_CD-1 downto 0) <=rx_data_i(IREGS_Ad_bits+2 downto 3)&filler(STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0);--Starting register address  	
--													hold_addr_s <= (others => '0');
													ins_addr_o(INS_ADDR_CI-1 downto 0) <=rx_data_i(IREGS_Ad_bits+2 downto 3)&filler( STRIPS_Ad_bits+TILES_Ad_bits-1 downto 0);--Starting register address  	

													count_s	<= (others =>'0');
													numregs_s <= 0;
													endreg_s <=rx_data_i(IREGS_Ad_bits*2+2 downto IREGS_Ad_bits+3); --Register address at which to terminate execution
													state <= RUN1;
			
											elsif rx_data_i(2 downto 0) = "100" then --OFLD
			
													rx_ack_o <= rx_valid_i;
													hold_addr_s(INS_ADDR_CD-1 downto 0) <=rx_data_i(INS_ADDR_CD+2 downto 3);	--Start address
													ins_addr_o(INS_ADDR_CD-1 downto 0) <=rx_data_i(INS_ADDR_CD+2 downto 3);	--Start address
													numregs_s <= conv_integer(rx_data_i(INS_ADDR_CD+3+DREGS_Ad_bits-1 downto INS_ADDR_CD+3));
													state <= OFLD;

													count_s	<= (others =>'0');
													endreg_s <= (others =>'0');
			
											else
													rx_ack_o <= rx_valid_i;
													hold_addr_s <= (others =>'0');
													count_s		<= (others =>'0');
													numregs_s	<= 0;
													endreg_s 	<= (others =>'0');

													if rx_valid_i = '1' then
															state <= CMD;
													else
															state <= IDL;
													end if;

											end if; --end rx_data(2:0) switch statement

									when LOAD_DATA =>

											--Outputs
											status_o	<= "0011";

											ins_data_o	<= rx_data_i(DATA_SIZE_C-1 downto 0);
											ins_addr_o	<= hold_addr_s;

											--Signals
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											flcount_s	<= "000";
											tog <= '0';
											tx_data_s <= X"000000000000000B";
  			
											if count_s(SC_LEN-INS_ADDR_CD-3-1 downto 0)  =  conv_std_logic_vector(0,SC_LEN-INS_ADDR_CD-3) then
													
													state <= IDL;
--													tx_data_s <= X"0000000000000000";
													ins_ctrl_o <= "000";
													count_s <= count_s;
													hold_addr_s <= hold_addr_s;
													rx_ack_o <= '0';
											else
													rx_ack_o	<= rx_valid_i;

													if rx_valid_i = '0' then
															state <= LD_FM;
--															tx_data_s <= X"000000000000000B";
															ins_ctrl_o <= "000";
															count_s <= count_s;
															hold_addr_s <= hold_addr_s;

													else
															state <= LOAD_DATA; 
--															tx_data_s <= X"0000000000000000";
															ins_ctrl_o	<= "010";
															count_s		<= count_s-1;
															inc_Daddress(hold_addr_s(INS_ADDR_C-1 downto 0));

													end if;
											end if;

									when LD_FM =>

											--Outputs
											status_o	<= "0100";	
											ins_ctrl_o	<= "000";
											ins_data_o	<= (others =>'0');
				
											--Signals
											hold_addr_s <= hold_addr_s;
											count_s		<= count_s;
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											flcount_s	<= "000";
											tog <= '0';
											tx_data_s <= X"000000000000000B";

											if rx_valid_i = '1' then
													state <= LOAD_DATA;
													rx_ack_o <= '1';
													ins_addr_o <= hold_addr_s;
											else
													state <= LD_FM;
													rx_ack_o 	<= '0';
													ins_addr_o	<= (others =>'0');
											end if;

									when LI1 =>

											--Outputs
											status_o	<= "0101";
											rx_ack_o <= rx_valid_i;

											ins_data_o	<= rx_data_i(INSTR_WIDTH_C-1 downto INSTR_WIDTH_C-DATA_SIZE_C); -- rx_data(47:12)
											ins_addr_o	<= hold_addr_s;

											--Signals
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											flcount_s	<= "000";
											tog <= '0';
											count_s <= count_s;
											hold_addr_s <= hold_addr_s;
											tx_data_s <= X"000000000000000A";
  			
											if count_s(SC_LEN-INS_ADDR_CI-3-1 downto 0)  =  conv_std_logic_vector(0,SC_LEN-INS_ADDR_CI-3) then
													
													state <= IDL;
--													tx_data_s <= X"0000000000000000";
													ins_ctrl_o <= "000";
--													hold_addr_s <= hold_addr_s;
													
											else
													if rx_valid_i = '1' then

--															count_s		<= count_s-1;
															state <= LI2; 
--															tx_data_s <= X"0000000000000000";
															ins_ctrl_o	<= "001";
													else
															state <= LI_FM;
--															tx_data_s <= X"000000000000000A";
															ins_ctrl_o <= "000";

													end if;
											end if;

									when LI2 =>

											--Outputs
											status_o	<= "0110";
											rx_ack_o	<= '0';

											ins_data_o	<= rx_data_i(DATA_SIZE_C-1 downto 0);
											ins_addr_o	<= hold_addr_s;

											--Signals
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											flcount_s	<= "000";
											tog <= '0';
											tx_data_s <= X"000000000000000A";
  			
											if rx_valid_i = '1' then

													state <= LI1; 
--													tx_data_s <= X"0000000000000000";
													ins_ctrl_o	<= "011";
													count_s		<= count_s-1;
													inc_Iaddress(hold_addr_s(INS_ADDR_C-1 downto 0));
											else
													state <= LI_FM;
--													tx_data_s <= X"000000000000000A";
													ins_ctrl_o <= "000";
													count_s <= count_s;
													hold_addr_s <= hold_addr_s;

											end if;

									when LI_FM =>

											--Outputs
											status_o	<= "0111";	
											ins_ctrl_o	<= "000";
											ins_data_o	<= (others =>'0');
				
											--Signals
											hold_addr_s <= hold_addr_s;
											count_s		<= count_s;
											numregs_s	<= 0;
											endreg_s	<= (others =>'0');
											delay_s		<= 0;
											flcount_s	<= "000";
											tog <= '0';
											tx_data_s <= X"000000000000000A";

											if rx_valid_i = '1' then
													state <= LI1;
													rx_ack_o <= '0';
													ins_addr_o <= hold_addr_s;
											else
													state <= LI_FM;
													rx_ack_o 	<= '0';
													ins_addr_o	<= (others =>'0');
											end if;

									when RUN1 =>	--Fetch instruction
											rx_ack_o 	<= '0';
											flcount_s <= "000";
											tog <= '0';

											status_o <= "1000";
											ins_ctrl_o <= "110";
											ins_addr_o <= hold_addr_s;
											ins_data_o	<= (others =>'0');
											delay_s <= delay_s -1;
											
											hold_addr_s <= hold_addr_s;
											count_s <= (others => '0');
											numregs_s	<= 0;
											endreg_s	<= endreg_s;
											tx_data_s <= tx_data_s;
--											tx_data_s <= filler(63 downto DATA_SIZE_C)&CPO_data_i;
											if delay_s = 3 then
													state <= RUN2;
											else
													state <= RUN1;
											end if;

									when RUN2 => --Decode instruction and fetch data
											rx_ack_o 	<= '0';
											flcount_s <= "000";
											tog <= '0';

											status_o <= "1001";
											ins_ctrl_o <= "111";
											ins_addr_o <= hold_addr_s;
											ins_data_o	<= (others =>'0');
--											delay_s <= delay_s -1;
											
											hold_addr_s <= hold_addr_s;
											count_s <= (others => '0');
											numregs_s	<= 0;
											endreg_s	<= endreg_s;
--											tx_data_s <= filler(63 downto DATA_SIZE_C)&CPO_data_i;
											tx_data_s <= tx_data_s;

											if delay_s = 0 then
													state <= RUN3;
													delay_s <= delay_s;
											else
													state <= RUN2;
													delay_s <= delay_s -1;
											end if;

									when RUN3 => --Execute and save results
											ins_data_o	<= (others =>'0');
											rx_ack_o 	<= '0';
											flcount_s <= "000";
											tog <= '0';

											status_o <= "1010";
											delay_s <= 5;
											
											count_s <= (others => '0');
											numregs_s	<= 0;
											endreg_s	<= endreg_s;
											
--											--Instruction address control
											if branch_cont_i = '1' and ins_done_i(1) = '1' then

													ins_addr_o(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= branch_data_i;
													hold_addr_s(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= branch_data_i;-- +1;
--													hold_addr_s <= hold_addr_s;

											elsif branch_cont_i = '0' and ins_done_i(1) = '1' then
													ins_addr_o(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= hold_addr_s(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits)+1;
													hold_addr_s(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) <= hold_addr_s(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits)+1;
											else --branch = 1 and one = 0, bother = 0, other
													ins_addr_o <= hold_addr_s;
													hold_addr_s <= hold_addr_s;
											end if;


											--State control
											if ins_done_i = "11" then 		--Overflowed AND done 

													state <= IDL;
													ins_ctrl_o <= "000";

													tx_data_s <= X"000000000000000D";--Overflowed

											elsif ins_done_i = "10" then 	--Done with no overflow
											
													tx_data_s <= filler(63 downto DATA_SIZE_C)&CPO_data_i;

													if hold_addr_s(INS_ADDR_CI-1 downto INS_ADDR_CI-IREGS_Ad_bits) = endreg_s then --Finished program
																state <= FLUSH_O; --Transmit whatever's been stored in a CPO packet and add on the 'End of execution signal"
																ins_ctrl_o <= "000";
														else    
																state <= RUN1;
																ins_ctrl_o <= "110";
													end if;

											else 	--Not done

--													tx_data_s <= filler(63 downto DATA_SIZE_C)&CPO_data_i; --Just keep constant
													tx_data_s <= tx_data_s;
													ins_ctrl_o <= "101";
													state <= RUN3;
											end if;
											
									when OFLD =>
											rx_ack_o 	<= '0';
											status_o <= "1011";
											delay_s <= 0;
											flcount_s <= "000";
											tog <= '0';

											ins_ctrl_o <= "100";
											ins_addr_o <= hold_addr_s;
											ins_data_o	<= (others =>'0');

											tx_data_s(63 downto DATA_SIZE_C) <= (others=> '0');
											tx_data_s(DATA_SIZE_C-1 downto 0) <= dataCy_i;

											------------------------------------------------------------------
											--If on last address of a strip, wait 1 cycle to account for registering
											if hold_addr_s(INS_ADDR_CD-1 downto STRIPS_Ad_bits+TILES_Ad_bits) = ZERO_ADDRESS(INS_ADDR_CD-1 downto INS_ADDR_C-1-DREGS_Ad_bits) and tog = '0' then --If on last address of a strip
													tog <= '1';
													hold_addr_s <= hold_addr_s;
											else
													tog <= '0';
						  							dec_Daddress(hold_addr_s(INS_ADDR_CD-1 downto 0),numregs_s);
											end if;
											------------------------------------------------------------------

											--State
											if hold_addr_s = ZERO_ADDRESS then --Last address has been reached so flush pipeline
												   state <= OFLDFLUSH;
										    else
													state <= OFLD;
											end if;

									when OFLDFLUSH =>
											rx_ack_o <= '0';
											status_o <= "1100";
											delay_s <= 0;
											tog <= '0';

--											ins_ctrl_o <= "100";
											ins_ctrl_o <= "000";
											ins_addr_o <= hold_addr_s;
											ins_data_o	<= (others =>'0');
											hold_addr_s <= hold_addr_s; 


--											if flcount_s = "110" then	--Flushed pipeline, uncomment this and ** to put a specific word 4 words from the end of the last offload packet
											if flcount_s = "101" then	--Flushed pipeline
												state <= FLUSH_O;
												flcount_s <= "000";
												tx_data_s <= tx_data_s;
--												tx_data_s <= X"FFFFEEEEBBBBEEEE"; **

											else --Still flushing pipeline of last OFLD words	
												state <= OFLDFLUSH;
												flcount_s <= flcount_s+1;
												tx_data_s(63 downto DATA_SIZE_C) <= (others=> '0');
												tx_data_s(DATA_SIZE_C-1 downto 0) <= dataCy_i;
											end if;

									when FLUSH_O =>
											rx_ack_o <= '0';
											status_o <= "1101";
											delay_s <= 0;
											flcount_s <= "000";
											tog <= '0';
											
											ins_ctrl_o <= "000";
											ins_addr_o <= hold_addr_s;
											ins_data_o	<= (others =>'0');
											hold_addr_s <= hold_addr_s;

											tx_data_s <= X"BBBBEEEEAAAADDDD"; --Finished transmitting all copied out data

											state <= IDL;

									when others =>
											state <= IDL;
											--Outputs
											--rx_ack_o <= rx_ack_o
											--status_o <= status_o

											--Signals
							 				hold_addr_s 		<= hold_addr_s; 		
							 				count_s 			<= count_s; 			
							 				numregs_s			<= numregs_s;
											endreg_s			<= endreg_s;
											delay_s				<= delay_s;
											flcount_s			<= flcount_s;
							 				tx_data_s		    <= tx_data_s;		
											tog 				<= tog;

							end case; --State switch
					end if; --End reset
			end if; --End Rising_edge(clk)
	end process; --End MAIN_STATE_PROCESS:

TXRX_ST_PROCESS:
process (clk, reset_i)
--	   variable counter : integer range 63 downto 0 := 0;
begin
		if falling_edge(clk) then
				if reset_i = '1' then
						txrx_st <= idle;
						wait_s <= (others => '0');

						--Outputs
						tx_data_o <=  (others => '0');
						tx_valid_o <= '0';
						tx_end_of_frame_o <= '0';
		
						--Signals
						TXWcounter_s <= 0;
						TXFULL_counter_s <= (others => '0');
		
				else
						case (txrx_st) is
		
								when idle =>

										if state = IDL or state = LI_FM or state = LD_FM then
												wait_s <= wait_s+1;
										end if;

										--Outputs
										tx_data_o <=  (others => '0');
										tx_valid_o <= '0';
										tx_end_of_frame_o <= '0';
										
										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= TXFULL_counter_s;
				
										if state = RUN3 then --or state = RUN2 or state  = RUN1 then
												txrx_st <= WMR; --Get ready to pack a mid-run results packet (copy_out data)
		
										elsif  state = FLUSH_O then
												txrx_st <= CPKT;	--If system is flushing, pack final flush comms packet
		
										elsif state = OFLD then
												txrx_st <= POFLD;	--Go pack off load data and from there proceed to transmission

										elsif state  = IDL  or state = LI_FM or state = LD_FM then	--If the main FSM is just sitting in IDL, request more data once every 63 cycles
												if wait_s = X"FF" then
--												if wait_s = X"FFFFF" then
														txrx_st <= CPKT;	--Go pack a communication packet requesting a response from the host
												else
														txrx_st <= idle;	--Continue waiting
												end if;

										else
												txrx_st <= idle;
										end if;
		
								when WMR => --Wait for mid-run results (get ready)
										--Outputs
--										tx_data_o <= (others => '0');
										tx_data_o <= tx_data_s;
										tx_valid_o <= '0';
										tx_end_of_frame_o <= '0';

										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= TXFULL_counter_s;

										if ins_done_i = "11" then -- Overflowed and done
												txrx_st <= CPKT;
										elsif ins_done_i = "10" then --Done with no overflow
												if CPO_ctrl_i = '1' then --Done, no overflow and CPO_ctrl high
														if TXFULL_counter_s = TXFULL then --Almost full so make this the last word in the packet and send
																txrx_st <= PTMR;
														else
																txrx_st <= PMR;
														end if;
												else --Done, no overflow but CPO_ctrl_i is low
														txrx_st <= idle;
												end if;

										else --Not done or overflowed and all other states
												txrx_st <= WMR;
										end if;


--										---------------------------------------------------------------------------------------------
--										--If tx almost full go to transmit packet regardless
--										if TXFULL_counter_s = TXFULL and ((ins_done_i = "00" and CPO_ctrl_i = '0') or(ins_done_i = "00" and CPO_ctrl_i = '1') or(ins_done_i = "01" and CPO_ctrl_i = '0') or(ins_done_i = "01" and CPO_ctrl_i = '1') or(ins_done_i = "10" and CPO_ctrl_i = '0') or(ins_done_i = "10" and CPO_ctrl_i = '1') or(ins_done_i = "11" and CPO_ctrl_i = '0') or(ins_done_i = "11" and CPO_ctrl_i = '1')) then
--												txrx_st <= TPKT;
--										
--										--Else if not almost full, if done and NOT overflowed and COPY_OUT is high go to pack mid run results
--										elsif TXFULL_counter_s /= TXFULL and ins_done_i = "10" and CPO_ctrl_i = '1' then
--												txrx_st <= PMR;
--
--										--Else if not close to full and overflowed go to pack communications packet
--										elsif TXFULL_counter_s /= TXFULL and ((ins_done_i = "11" and CPO_ctrl_i = '0')or(ins_done_i = "11" and CPO_ctrl_i = '1')) then
--												txrx_st <= CPKT;
--
--										--Else if not almost full, not overflowed, not copy out but IS done then back to idle to start again
--										elsif TXFULL_counter_s /= TXFULL and ins_done_i = "10" and CPO_ctrl_i = '0' then
--												txrx_st <=  idle;
--
--										--If anything else just hang around in waiting for mid-run result
--										else
--												txrx_st <= WMR;
--										end if;
										---------------------------------------------------------------------------------------------
--										Logic above is based on (which takes into account every possibility, it's just been re-ordered hencing not apprearing so)
--										NEXT
--										txrx_st		done	oob		cpo_ctrl	tx_afull
--										TPKT		0		0		0			1
--										TPKT		0		0		1			1
--										TPKT		0		1		0			1
--										TPKT		0		1		1			1
--										TPKT		1		0		0			1
--										TPKT		1		0		1			1
--										TPKT		1		1		0			1
--										TPKT		1		1		1			1
--															
--										WMR			0		0		0			0
--										WMR			0		0		1			0
--													 	   	 	   
--										PMR			1		0		1			0
--													 	   	
--													 	   	
--										WMR			0		1		0			0
--										WMR			0		1		1			0
--										CPKT		1		1		0			0
--										CPKT		1		1		1			0
--													 	   	
--										IDL			1		0		0			0
--										---------------------------------------------------------------------------------------------
										
								when PMR =>	--Pack mid-run results
										--Outputs
										tx_data_o <= tx_data_s;
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '0';

										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= TXFULL_counter_s+1;

										txrx_st <= idle;

								when PTMR =>	--Pack and transmit mid-run results
										--Outputs
										tx_data_o <= tx_data_s;
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '1';

										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= (others => '0');

										txrx_st <= idle;

		
								when CPKT => --Pack a communications packet
		
										--Outputs
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '0';
		
										TXWcounter_s <= TXWcounter_s +1;


										if TXWcounter_s = 0 then	--Could add another signal 'tx_coms_data_s' and use it to store ts_data_s and send that to tx_data_o after 1st cycle but think this should work as is
												tx_data_o <= tx_data_s;
										else
--												tx_data_o <= tx_data_o;
										end if;


										if TXWcounter_s = 2 then
												txrx_st <= TPKT;
										else
												txrx_st <= CPKT;
										end if;

										TXFULL_counter_s <= TXFULL_counter_s;


								when POFLD => --Pack off load data
										tx_data_o <= tx_data_s;
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '0';


										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= TXFULL_counter_s+1;


										--State
										if state = FLUSH_O then

												txrx_st <= CPKT;

										else

												if TXFULL_counter_s = TXFULL then
														txrx_st <= BTPKT;
												else
														txrx_st <= POFLD;
												end if;
										end if;

								when BTPKT => --Transmit packet
										--Outputs
										tx_data_o <=  tx_data_s;
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '1';
										
										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= (others => '0');

										if state = FLUSH_O then
												txrx_st <= CPKT;
										else
												txrx_st <= POFLD;
										end if;
		
								when TPKT => --Transmit packet
										--Outputs
										tx_data_o <=  X"FFEEAADDFFEEAADD";--a distinctive NAN signalling the end of a packet
										tx_valid_o <= '1';
										tx_end_of_frame_o <= '1';
										
										--Signals
										TXWcounter_s <= 0;
										TXFULL_counter_s <= (others => '0');

										txrx_st <= idle;

		
								when others =>
										txrx_st <= idle;
										TXWcounter_s <= TXWcounter_s;
										TXFULL_counter_s <= TXFULL_counter_s;
		
										---TEST, shouldn't need there-------
										tx_end_of_frame_o <= '0';
										tx_data_o <= X"0000000000000000";
										tx_valid_o <= '0';
										-------------------------------
				
						end case;--End txrx_st switch
				end if; --End reset
		end if; --End rising_edge(clk)
end process; --End TXRX_ST_PROCESS



end behavioural;

