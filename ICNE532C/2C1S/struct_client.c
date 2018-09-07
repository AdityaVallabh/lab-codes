// Client side implementation of UDP client-server model
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
 
typedef struct {
    char c;
    int n;
    float f;
} Packet;

// Driver code
int main() {
    int sockfd;
    char buffer[MAXLINE];
    char *msg;
    struct sockaddr_in     servaddr;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
 
    memset(&servaddr, 0, sizeof(servaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    servaddr.sin_addr.s_addr = INADDR_ANY;
     
    int n, len;
    Packet pkt;
    
    printf("pkt.c: ");
    scanf("%c", &pkt.c);
    printf("pkt.n: ");
    scanf("%d", &pkt.n);
    printf("pkt.f: ");
    scanf("%f", &pkt.f);
    sendto(sockfd, (const Packet *) &pkt, sizeof(Packet), MSG_CONFIRM, (const struct sockaddr *) &servaddr, sizeof(servaddr));
    printf("Sent : (%c, %d, %f)\n", pkt.c, pkt.n, pkt.f);

    n = recvfrom(sockfd, (Packet *) &pkt, sizeof(Packet), MSG_WAITALL, (struct sockaddr *) &servaddr, &len);
    printf("Server : (%c, %d, %f)\n", pkt.c, pkt.n, pkt.f);

    close(sockfd);

    return 0;
}