from threading import Thread
import sys
import socket
import os

class Client(Thread):

    def __init__(self, host, port):
        super(Client, self).__init__()
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self):
        print('Connected')
        while True:
            data = self.server.recv(1024).decode()
            if not data:
                os._exit(0)
            print("<- {}".format(data))

class Server(Thread):

    def __init__(self, host, port):
        super(Server, self).__init__()
        self.host = host
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # waiting for a connection
        print("Waiting for connection on port {}...".format(port))
        self.client, addr = sock.accept()
        print("{} connected".format(addr))

    def run(self):
        while True:
            data = self.client.recv(1024).decode()
            if not data:
                os._exit(0)
            print("<- {}".format(data))

if len(sys.argv) > 1 and sys.argv[1] == 'connect':
    host = input("Host: ")
    port = int(input("Port: "))
    client = Client(host, port)
    client.start()
    while True:
        data = input()
        if data == 'quit':
            os._exit(0)
        print("-> {}".format(data))
        client.server.sendall(data.encode())
else:
    host = input("Host: ")
    port = int(input("Port: "))
    server = Server(host, port)
    server.start()
    while True:
        data = input()
        if data == 'quit':
            os._exit(0)
        print("-> {}".format(data))
        server.client.sendall(data.encode())
    
