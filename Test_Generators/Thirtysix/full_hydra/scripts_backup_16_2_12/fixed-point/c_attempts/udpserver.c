/* udpreceive.c */ 

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

unsigned long return_LI[] = {10};
unsigned long return_LD[] = {11};
unsigned long return_done[] = {12};

int main()
{
        int s_sock, r_sock;
        int addr_len, bytes_read;
        char recv_data[1024];
        struct hostent *host;
        struct sockaddr_in receive_addr , send_addr;

		host = (struct hostent*) gethostbyname((char*) "10.128.23.173");

		//Create sockets
        if ((r_sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
            perror("Receive Socket");
            exit(1);
        }

        if ((s_sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
            perror("Send Socket");
            exit(1);
        }

        receive_addr.sin_family = AF_INET;
        receive_addr.sin_port = htons(3157);
        receive_addr.sin_addr.s_addr = INADDR_ANY;
        bzero(&(receive_addr.sin_zero),8);

		send_addr.sin_family = AF_INET;
        send_addr.sin_port = htons(3158);
        
        send_addr.sin_addr = *((struct in_addr *)host->h_addr);
        bzero(&(send_addr.sin_zero),8);
        

        if (bind(r_sock,(struct sockaddr *)&receive_addr,
            sizeof(struct sockaddr)) == -1)
        {
            perror("Bind receive socket");
            exit(1);
        }

        addr_len = sizeof(struct sockaddr);
		
		printf("\nReady to send data on port %d", ntohs(send_addr.sin_port));
		printf("\nWaiting to receive data on port %d", ntohs(receive_addr.sin_port));
        fflush(stdout);

		int count = 0;
		int a = 0;

		while (1)
		{

			bytes_read = recvfrom(r_sock,recv_data,9000,0, (struct sockaddr *)&receive_addr, &addr_len);

	  		fflush(stdout);

			if (count < 2){
			  		sendto(s_sock, return_LI, sizeof(return_LI), 0, (struct sockaddr *)&send_addr, sizeof(struct sockaddr));
			}
			else if (count < 4){
			  		sendto(s_sock, return_LD, sizeof(return_LD), 0, (struct sockaddr *)&send_addr, sizeof(struct sockaddr));
					
			}
			else if (count < 6){
			  		sendto(s_sock, return_done, sizeof(return_done), 0, (struct sockaddr *)&send_addr, sizeof(struct sockaddr));
					count = -1;
			}
			
			count =count+1;
			printf("\ncount: %d",count);
        }
        
        return 0;
}
