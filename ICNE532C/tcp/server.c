#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 8080
int main(int argc, char const *argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    char *msg;
      
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );
      
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 1);

    while(1) {
        printf("[*] Waiting for connection...\n");
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        inet_ntop(AF_INET, &(address.sin_addr), buffer, addrlen);
        printf("[*] New client connected: %s\n", buffer);
        while(1) {
            valread = read( new_socket , buffer, 1024);
            buffer[valread] = '\0';
            if (valread == 0) break;
            printf("Client: %s\n", buffer);
            printf("You: ");
            scanf("%s", msg);
            send(new_socket , msg , strlen(msg) , 0 );            
        }
        printf("[*] Client disconnected\n");
    }
    return 0;
}
