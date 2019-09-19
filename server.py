import socket
from threading import Thread
from random import randint
from ast import literal_eval

clients = {}
address = {}
tcp_ip = '0.0.0.0'
tcp_port = 9898
buffer = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip,tcp_port))

#Add a feature that imports the dict from a file, make it do ports to so you can have multiple running on one computer
#filee = open('ips.txt','r')
#ips = eval(filee.read())
#filee.close()

class Client(Thread):

    def __innit__(self,ip,port,buffer):
        Thread.__innit__(self)
        self.ip = ip
        self.port = port
        self.buffer = buffer
        print ('New connection from ', ip)

    def handle_colour():
        #colourss = open('colours.txt','r')
        #colours = literal_eval(colourss.read())
        #colourss.close()
        colours=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']
        random = randint(0,19)
        colour = colours[random]
        colours.pop(random)
        print(colour)
        return colour
    
    def broadcast(msg, colour='', prefix=''):
        '''Broadcasts a message to all the clients dat are connected'''
        prefix = colour+prefix
        clientstopop=[]
        for sock in clients:
            try:
                sock.send(bytes(prefix, 'utf8')+msg)
            except ConnectionResetError:
                clientstopop.append(sock)
                pass

        for i in clientstopop:
            clients.pop(sock)

    def handle_client(client):
        '''Handles a clients dat are already connection'''
        name = client.recv(buffer).decode('utf8')
        welcome = '00 \nWelcome %s! If you ever want to quit (which you never will), type /quit to exit \n' % name
        client.send(bytes(welcome, 'utf8'))
        mssg = '00%s has joined the chat!' % name
        Client.broadcast(bytes(mssg, 'utf8'))
        clients[client] = name
        colour = Client.handle_colour()
        while True:
            msg = client.recv(buffer)
            if msg != bytes('/quit', 'utf8'):
                Client.broadcast(msg, colour, name+': ')
            else:
                #Commented out the next line because I think it is handled by the client
                #client.send(bytes('/quit', 'utf8'))
                client.close()
                del clients[client]
                Client.broadcast(bytes('00%s has left the chat.' % name, 'utf8'))
                break

    def accept_incoming_connections():
        while True:
            client, client_address = server.accept()
            print('%s:%s has connected.' % client_address)
            client.send(bytes('00Welcome to this super epic chat room by me. '+
                              'Type your name and press enter in the box provided below', 'utf8'))
            address[client] = client_address
            Thread(target=Client.handle_client, args=(client,)).start()        


if __name__ == '__main__':
    server.listen(4)  # Listening for up to 4 connections
    print('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=Client.accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
