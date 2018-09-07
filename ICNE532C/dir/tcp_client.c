// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 8080
  
int main(int argc, char const *argv[])
{
    struct sockaddr_in serv_addr;
    int sock = 0, valread;
    char *msg;
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
  
    memset(&serv_addr, '0', sizeof(serv_addr));
  
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
      
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);  
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }
    printf("[*] Connected to server\n");    
    while(1) {
        printf("You: ");
        scanf("%s", msg);
        if (strcmp(msg, "exit") == 0) break;
        send(sock , msg , strlen(msg) , 0 );
        valread = read( sock , buffer, 1024);
        buffer[valread] = '\0';
        if (valread == 0) break;
        printf("Server: %s\n",buffer );
    }
    printf("[*] Session disconnected\n");
    return 0;
}
