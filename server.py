import socket
from threading import Thread
from random import randint
from ast import literal_eval
import tkinter
import sqlite3

clients = {}
address = {}
tcp_ip = '0.0.0.0'
tcp_port = 9898
buffer = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip,tcp_port))

class Client(Thread):

    def __innit__(self,ip,port,buffer):
        Thread.__innit__(self)
        self.ip = ip
        self.port = port
        self.buffer = buffer
        self.colour = ''
        print ('New connection from ', ip)

    def command(msg, client, colour, auth):
        message = msg.decode('utf8')    
        message = message.split(' ')
        print(message)

        if message[0][1:] == 'help':
            f = open('help.txt')
            readme = f.read()
            f.close()
            client.send(bytes('99'+readme+'\n', 'utf-8'))

        if message[0][1:] == 'broadcast':
            if auth == True:
                for sock in clients:
                    try:
                        sock.send(bytes('99!!'+','.join(message[1:]), 'utf8'))
                    except ConnectionResetError:
                        clientstopop.append(sock)
                        pass
            
        if message[0][1:] == 'sudo':
            try:
                password = message[1]
                dbconn = sqlite3.connect('sudo.db')
                c = dbconn.cursor()
                c.execute("SELECT * FROM sudo")
                correctpasswords = c.fetchall()
                print(correctpasswords)
                dbconn.close()
                for password in correctpasswords:
                    #the passwords should be stored hashed at some point
                    pass
                if password in correctpasswords:
                    auth = True
                print (auth)
            except IndexError:
                client.send(bytes('99Correct usage is /sudo [password]', 'utf-8'))
            
        if message[0][1:] == 'colour':
            try:
                print('try')
                arg1=int(message[1])
                print(type(arg1))
                if 1 <= arg1 <= 20:
                    colour = message[1]
                    print('debug2'+colour)
                    if len(colour) != 2:
                        colour = '0'+colour
                        print('debug3'+colour)
                        client.send(bytes(colour+'Colour successfully changed\n', 'utf-8'))
                    else:
                        print('debug4'+colour)
                        client.send(bytes(colour+'Colour successfully changed\n', 'utf-8'))
            except:
                pass
            
        return (colour, auth)
                

    def handle_colour():
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
        welcome = '00Welcome %s! Type /help to view the commands \n' % name
        auth = False
        client.send(bytes(welcome, 'utf8'))
        mssg = '00%s has joined the chat!\n' % name
        Client.broadcast(bytes(mssg, 'utf8'))
        clients[client] = name
        colour = Client.handle_colour()
        while True:
            msg = client.recv(buffer)
            if msg[0] != 47:
                print(colour)
                Client.broadcast(msg, colour, name+': ')
            else:
                #Commented out the next line because I think it is handled by the client
                #client.send(bytes('/quit', 'utf8'))
                returned = Client.command(msg, client, colour, auth)
                colour = returned[0]
                auth = returned[1]
                
                '''client.close()
                del clients[client]
                Client.broadcast(bytes('00%s has left the chat.' % name, 'utf8'))'''
                

    def accept_incoming_connections():
        while True:
            client, client_address = server.accept()
            print('%s:%s has connected.' % client_address)
            client.send(bytes('00Welcome to this super epic chat room by me. '+
                              'Type your name and press enter in the box provided below\n', 'utf8'))
            address[client] = client_address
            Thread(target=Client.handle_client, args=(client,)).start()        


if __name__ == '__main__':
    server.listen(4)  # Listening for up to 4 connections
    print('Waiting for connection...')
    #screen = Monitor.run()
    ACCEPT_THREAD = Thread(target=Client.accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()

