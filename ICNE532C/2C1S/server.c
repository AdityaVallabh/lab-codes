#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
 
#define PORT     8080
#define MAXLINE 1024

struct node {
    char host[50];
    int port;
};

int main() {
    int sockfd;
    char buffer[MAXLINE];
    char msg[1024];
    struct sockaddr_in servaddr, cliaddr, cliaddr1, cliaddr2;
    int c1 = 0, c2 = 0;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
     
    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));
    memset(&cliaddr1, 0, sizeof(cliaddr1));
    memset(&cliaddr2, 0, sizeof(cliaddr2));

    servaddr.sin_family    = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
     
    int len, n = 0;

    strcpy(msg, "accepted");

    sendto(sockfd, (const char *) msg, strlen(msg), MSG_CONFIRM, (const struct sockaddr *) &servaddr, sizeof(servaddr));
    recvfrom(sockfd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr1, &len);

    recvfrom(sockfd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr1, &len);buffer[n] = '\0';
    printf("%s-%d : %s\n", inet_ntoa(cliaddr1.sin_addr), ntohs(cliaddr1.sin_port), buffer);
    recvfrom(sockfd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr2, &len);buffer[n] = '\0';
    printf("%s-%d : %s\n", inet_ntoa(cliaddr2.sin_addr), ntohs(cliaddr2.sin_port), buffer);

    sendto(sockfd, (const char *)msg, strlen(msg), MSG_CONFIRM, (const struct sockaddr *) &cliaddr1, len);
    sendto(sockfd, (const char *)msg, strlen(msg), MSG_CONFIRM, (const struct sockaddr *) &cliaddr2, len);
    
    while(1) {        
        n = recvfrom(sockfd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr, &len);
        buffer[n] = '\0';
        for(int i = 0; i < n; i++) {
            buffer[i] -= 1;
        }
        if(strcmp(inet_ntoa(cliaddr.sin_addr), inet_ntoa(cliaddr1.sin_addr)) == 0 && cliaddr.sin_port == cliaddr1.sin_port) {
            sendto(sockfd, (const char *)buffer, strlen(buffer), MSG_CONFIRM, (const struct sockaddr *) &cliaddr2, len);
        }
        else if(strcmp(inet_ntoa(cliaddr.sin_addr), inet_ntoa(cliaddr2.sin_addr)) == 0 && cliaddr.sin_port == cliaddr2.sin_port) {
            sendto(sockfd, (const char *)buffer, strlen(buffer), MSG_CONFIRM, (const struct sockaddr *) &cliaddr1, len);
        }
    }
     
    return 0;
}