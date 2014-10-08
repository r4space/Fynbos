#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <sstream>
#include <iostream>
#include <fstream>
#include <iomanip>
using namespace std;

int main()
{
//////Create sockets
	int r_sock, s_sock;
	int bytes_read;
	socklen_t addr_len;
	struct sockaddr_in server_addr, receive_addr;
	struct hostent *host;
	unsigned long recv_data[1125];//1125 being the theoretical maximum number of longs that a packet could hold(more than enough therefore)

	
	host= (struct hostent *) gethostbyname((char *)"10.128.23.204");

	if ((r_sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1)
	{
		perror("Receive socket");
		exit(1);
	}
	
	if ((s_sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1)
	{
		perror("Send socket");
		exit(1);
	}

	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(3157);
	server_addr.sin_addr = *((struct in_addr *)host->h_addr);
	bzero(&(server_addr.sin_zero),8);
	
	receive_addr.sin_family = AF_INET;
	receive_addr.sin_port = htons(3158);
	receive_addr.sin_addr.s_addr = INADDR_ANY;
	bzero(&(receive_addr.sin_zero),8);

	if(bind(r_sock, (struct sockaddr*) &receive_addr, sizeof(struct sockaddr)) == -1)
	{
		perror("Bind Receive socket");
		exit(1);
	}
	
	addr_len =(socklen_t )sizeof(struct sockaddr);
	
//////Send data and instructions to roach
	ifstream dataF("data.txt");
	//Check input data file isn't already open
	if (!dataF.is_open()){
			printf("The data.txt file could not be opened exiting");
			exit(1);
	}

	string packet = "";
	const char * msg;
	int len,z=0,d =0;
	while (1)
	{
			getline(dataF,packet);

			if (dataF.eof()){
					cout<<"got to end of file\n";
					break;}
			else
			{		//Send a line(packet) from file
					len=packet.length();
					msg=packet.c_str();
					cout <<"\nSending packet "<<d<<" of length "<<len<<"";
					sendto(s_sock, msg, len, 0, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));

					//Wait for a response and interpret it
					bytes_read = recvfrom(r_sock, recv_data,9000, 0, (struct sockaddr *)&receive_addr, &addr_len);
			}
			d++;
	}
	dataF.close();

//////Receive data

	int k,j =0;
	int bytes_read_arr[500];	//Excesssively large int array to store how many bytes were received in each packet for post-processing purposes
	unsigned long *buffer;
	buffer=(unsigned long*)malloc(500*1125*sizeof(unsigned long));
	cout<<"\nsize of unl: "<<sizeof(unsigned long);
	if (buffer==NULL) exit(1);
	while(1){

			bytes_read_arr[j] = recvfrom(r_sock,(unsigned long*)(buffer+j*1125), 9000, 0, (struct sockaddr *)&receive_addr, &addr_len);

			//Check for control signalling the end of data
			if ((bytes_read_arr[j]==24)and(*(buffer+j*1125)==12))
					break;
			j++;
	}

//////Post processing of results
	ofstream resultsF("results");
	printf("\nProcessing results received");
	for (k=0; k<j;k++)
	{
			resultsF<<"\n";
			for (int f =0; f<bytes_read_arr[k]/8;f++)
			{
					resultsF<<"\n";
					resultsF<<*(buffer+k*1125+f);
			}
	}

	free(buffer);
	resultsF.close();
	fflush(stdout);
}

