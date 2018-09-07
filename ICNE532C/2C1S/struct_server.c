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

int main() {
    int sockfd, len;
    char buffer[MAXLINE];
    char msg[1024];
    struct sockaddr_in servaddr, cliaddr, cliaddr1, cliaddr2;
    Packet pkt1, pkt2;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
     
    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));
    memset(&cliaddr1, 0, sizeof(cliaddr1));
    memset(&cliaddr2, 0, sizeof(cliaddr2));
    memset(buffer, 0, MAXLINE);

    servaddr.sin_family    = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(PORT);

    bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
    sendto(sockfd, (const char *) buffer, 0, MSG_CONFIRM, (const struct sockaddr *) &servaddr, sizeof(servaddr));
    recvfrom(sockfd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr1, &len);

    printf("Waiting...\n");
    recvfrom(sockfd, (Packet *) &pkt1, sizeof(Packet), MSG_WAITALL, ( struct sockaddr *) &cliaddr1, &len);
    printf("%s-%d: (%c, %d, %f)\n", inet_ntoa(cliaddr1.sin_addr), ntohs(cliaddr1.sin_port), pkt1.c, pkt1.n, pkt1.f);
    recvfrom(sockfd, (Packet *) &pkt2, sizeof(Packet), MSG_WAITALL, ( struct sockaddr *) &cliaddr2, &len);
    printf("%s-%d: (%c, %d, %f)\n", inet_ntoa(cliaddr2.sin_addr), ntohs(cliaddr2.sin_port), pkt2.c, pkt2.n, pkt2.f);

    pkt1.c += 01, pkt2.c += 01;
    pkt1.n -= 10, pkt2.n -= 10;
    pkt1.f *= 02, pkt2.f *= 02;

    sendto(sockfd, (const char *) &pkt2, sizeof(Packet), MSG_CONFIRM, (const struct sockaddr *) &cliaddr1, len);
    sendto(sockfd, (const char *) &pkt1, sizeof(Packet), MSG_CONFIRM, (const struct sockaddr *) &cliaddr2, len);
     
    return 0;
}