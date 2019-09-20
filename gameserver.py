import socket
import random
from threading import Thread

clients = {}
address = {}
tcp_ip = '0.0.0.0'
tcp_port = 9899
buffer = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip, tcp_port))

deck = ['1s','2s','3s','Js','Qs','Ks']

class Client(Thread):
    
    def __innit__(self,ip,port,buffer):
        Thread.__innit__(self)
        self.ip = ip
        self.port = port
        self.buffer = buffer
        print ('New connection from ', ip)

    def broadcast(msg):
        '''Broadcasts a message to all the clients dat are connected'''
        clientstopop = []
        for sock in clients:
            try:
                sock.send(bytes(msg,'utf8'))
            except ConnectionResetError:
                clientstopop.append(sock)
                pass

    def handle_client(client):
        '''Handles a clients dat are already connection'''
        name = client.recv(buffer).decode('utf8')
        clients[client] = name
        if len(clients) < 4:
            client.send(bytes('waiting4players','utf8'))
        else:
            Client.broadcast('4players')
        while True:
            msg = client.recv(buffer)
            if msg != bytes('/quit', 'utf8'):
                pass
            else: client.close()
            del clients[client]
            Client.broadcast(bytes('leftgame','utf8'))
            break

    def accept_incoming_connections():
        while True:
            client, client_address = server.accept()
            print('%s:%s has connected.' % client_address)
            client.send(bytes('What is your player name?','utf8'))
            address[client] = client_address
            Thread(target=Client.handle_client, args=(client,)).start()

if __name__ == '__main__':
    server.listen(4)
    print('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=Client.accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()

            
