#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#define PORT 8080

struct Entry {
    int n;
    char name[50];
};

struct Entry* read_file(char *file_name, struct Entry *entries, int *num, char *data) {
    FILE *fp;
    char buff[255];
    int n, i = 0;

    fp = fopen(file_name, "r");

    while(fscanf(fp, "%d%s\n", &n, buff) == 2) {
       // printf("%d: %s\n", n, buff);
       sprintf(data, "%s%d: %s\n", data, n, buff);
       entries[i].n = n;
       strcpy(entries[i].name, buff);
       i += 1;
    }

    *num = i;
    return entries;
}

int main(int argc, char const *argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    char msg[1024], data[1024];
    struct Entry entries[10];
    int n, i;
    data[0] = '\0';

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );
      
    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 1);
    read_file("dir.txt", entries, &n, data);
    // printf("Directory %d: \n%s\n", n, data);
    for(i = 0; i < n; i++) {
        printf("%d: %s\n", entries[i].n, entries[i].name);
    }
    while(1) {
        printf("[*] Waiting for connection...\n");
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        inet_ntop(AF_INET, &(address.sin_addr), buffer, addrlen);
        printf("[*] New client connected: %s\n", buffer);
        while(1) {
            valread = read( new_socket , buffer, 1024);
            buffer[valread] = '\0';
            if (valread == 0) break;
            if(strcmp(buffer, "ls") == 0) {
                strcpy(msg, data);
            } else {
                int x = atoi(buffer);
                printf("%d ", x);
                i = (x == 0 && buffer[0] != '0')? n : 0;
                for(; i < n; i++) {
                    if(entries[i].n == x) {
                        strcpy(msg, entries[i].name);
                        break;
                    }
                }
                if(i == n) strcpy(msg, "Address not found");
            }

            // printf("Client: %s\n", buffer);
            // printf("You: ");
            // scanf("%s", msg);
            send(new_socket , msg , strlen(msg) , 0 );
            fflush(stdout);         
        }
        printf("[*] Client disconnected\n");
    }
    return 0;
}
