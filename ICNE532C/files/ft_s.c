#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <unistd.h> 
  
#define IP_PROTOCOL 0 
#define PORT_NO 8083
#define NET_BUF_SIZE 32
#define nofile "File Not Found!" 
  
// funtion to clear buffer 
void clearBuf(char* b) 
{ 
    int i; 
    for (i = 0; i < NET_BUF_SIZE; i++) 
        b[i] = '\0'; 
}
  
// funtion sending file 
int sendFile(FILE* fp, char* buf, int s) 
{ 
    int i, len; 
    if (fp == NULL) { 
        strcpy(buf, nofile); 
        len = strlen(nofile); 
        buf[len] = EOF;
        return 1; 
    } 
  
    char ch, ch2; 
    for (i = 0; i < s; i++) { 
        ch = fgetc(fp); 
        ch2 = ch; 
        buf[i] = ch2; 
        if (ch == EOF) 
            return 1; 
    } 
    return 0; 
} 
  
// driver code 
int main() 
{ 
    int sockfd, nBytes, new_socket; 
    struct sockaddr_in addr_con; 
    int addrlen = sizeof(addr_con); 
    addr_con.sin_family = AF_INET; 
    addr_con.sin_port = htons(PORT_NO); 
    addr_con.sin_addr.s_addr = INADDR_ANY; 
    char net_buf[NET_BUF_SIZE]; 
    FILE* fp; 
  
    // socket() 
    sockfd = socket(AF_INET, SOCK_STREAM, 0); 
  
    if (sockfd < 0) 
        printf("\nfile descriptor not received!!\n"); 
    else
        printf("\nfile descriptor %d received\n", sockfd); 
  
    // bind() 
    if (bind(sockfd, (struct sockaddr*)&addr_con, sizeof(addr_con)) == 0) 
        printf("\nSuccessfully binded!\n"); 
    else
        printf("\nBinding Failed!\n"); 
    listen(sockfd, 3);
    while (1) { 
        printf("\nWaiting for file name...\n"); 
  
        // receive file name 
        clearBuf(net_buf); 
  
        new_socket = accept(sockfd,  
                    (struct sockaddr *)&addr_con, (socklen_t*)&addrlen);
        if(fork() == 0) continue;
        nBytes = read( new_socket , net_buf, 1024);
        net_buf[nBytes-1] = '\0';
        fp = fopen(net_buf, "r"); 
        printf("\nFile Name Received: %s,%d\n", net_buf, strlen(net_buf)); 
        if (fp == NULL) 
            printf("\nFile open failed!\n"); 
        else
            printf("\nFile Successfully opened!\n"); 
  
        while (1) { 
            // process 
            if (sendFile(fp, net_buf, NET_BUF_SIZE)) {
                send(new_socket , net_buf , NET_BUF_SIZE , 0 );
                break; 
            } 
  
            // send 
            send(new_socket , net_buf , NET_BUF_SIZE , 0 );
            clearBuf(net_buf); 
        } 
        if (fp != NULL) 
            fclose(fp); 
    } 
    return 0; 
} 
