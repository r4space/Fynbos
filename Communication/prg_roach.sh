#!/bin/sh

BOF=6x5x27x1024.bof #sxtxdxdrxir
#XPS=/home/jwyngaard/active_ise/TenGbPlus/core10Gb		# Directory in which cor_info.tab is located
#PRJBIN=/home/jwyngaard/active_ise/TenGbPlus/top_level.bin	#.bin file to be used

#if [ $1 -eq 1] 
#then
	echo "Making bof file now"
#	wine mkbof.exe -o $BOF -s ./simple_top_XPS/XPS_ROACH_base/core_info.tab -t 3 ./simpleTop/top_level.bin
	./mkbof -o ./copybofs/$BOF -s ./bofInputs/core_info.tab -t 3 ./bofInputs/top_level.bin

	echo "copying and chmod'ing bof file to srv"
	cp -i ./copybofs/$BOF /srv/roach_boot/etch/boffiles/
	chmod u+x /srv/roach_boot/etch/boffiles/$BOF

	echo "Run roach programing script: "
	./j.py -r 192.168.100.100 -i 167772171 -p 3157 -a 167772161 -o 3158

#else	
#	./j.py -r 192.168.100.100 -i 167772171 -p 3157 -a 167772161 -o 3158
#fi

