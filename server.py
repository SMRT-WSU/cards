import socket
from threading import Thread
from random import randint
from ast import literal_eval
import tkinter
import subprocess
import hashlib, binascii, os

clients = {}
address = {}
tcp_ip = '0.0.0.0'
tcp_port = 9898
buffer = 4096
admin = '3d119cdd6da93121cec83781782781e9a92fdbd013b30df94ab2144c26bb5fb8d47729cb0ffdba974205c0a113ef1b4121a3ccde1bc785f53a6836f7cb014c4f6b60c2c66e78024e35642b06fe312d07c75e70ca46e85817d49a7a68f206dfb1'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip,tcp_port))

#The following two functions have been taken from https://www.vitoshacademy.com/hashing-passwords-in-python/
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    print (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

class BadFormat(Exception):
    pass

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
            f = open('./data/help.txt')
            readme = f.read()
            f.close()
            client.send(bytes('99'+readme+'\n', 'utf-8'))

        if message[0][1:] == 'ls':
            try:
                ls = subprocess.check_output('powershell.exe ls ./downloads',shell=True,stderr=subprocess.STDOUT)
                print(str(client)+ls.decode('utf-8'))
                client.send(bytes('CO','utf-8')+ls+bytes('\n','utf-8'))
            except subprocess.CalledProcessError as e:
                print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            
        if message[0][1:] == '.':
            if auth == 2:
                args = ' '.join(message[1:])
                command = subprocess.check_output('powershell.exe '+args,shell=True,stderr=subprocess.STDOUT)
                client.send(bytes('CO','utf-8')+command+bytes('\n','utf-8'))
            else:
                client.send(bytes('99You are not privilaged to run this command\n','utf-8'))
        
        if message[0][1:] == 'upload':
            print('hi')
            try:
                #if len(message) is not 5:
                #    raise BadFormat
                filename = client.recv(64).decode('utf-8')
                filename = filename.replace(' ','')
                print ('hi'+filename)
                client.send(bytes('99Your file is being uploaded, please wait\n','utf-8'))
                a = False
                data = bytearray()
                while a is False:
                    data.extend(client.recv(buffer))
                    #print(data)
                    #print(data[-4:])
                    
                    if data[-4:] == b'AA01':
                        print('data ends in AA01')
                        data = data[:-4]
                        a = True
                print('escaped loop')
                f = open('./downloads/'+filename, 'wb')
                f.write(data)
                f.close
                client.send(bytes('99File Uploaded: '+filename+'\n', 'utf-8'))
            except BadFormat:
                client.send(bytes('99Correct format is /upload -p [filepath] -n [filename]\n', 'utf-8'))
            
        if message[0][1:] == 'broadcast':
            if auth == True:
                for sock in clients:
                    try:
                        sock.send(bytes('!!'+' '.join(message[1:])+'\n', 'utf8'))
                    except ConnectionResetError:
                        clientstopop.append(sock)
                        pass
            else:
                client.send(bytes('99You are not authorised to use this command\n', 'utf-8'))
            
        if message[0][1:] == 'sudo':
            try:
                password = message[1]
                print('password is '+password)
                f=open('./data/sudo.txt')
                correctpasswords = literal_eval(f.read())
                f.close()
                print(correctpasswords)
                if auth == 2:
                    client.send(bytes('99You already have higher level user access\n', 'utf-8'))
                elif verify_password(admin, password) == True:
                    auth = 2
                    client.send(bytes('99Authorised as higher level user\n','utf-8'))
                elif auth == 1:
                    client.send(bytes('99You are already authorised\n', 'utf-8'))
                else:
                    for i in correctpasswords:
                        print (i)
                        if password == i:
                            auth = 1
                            client.send(bytes('99Authorised\n','utf-8'))
                print (auth)
            except IndexError:
                client.send(bytes('99Correct usage is /sudo [password]\n', 'utf-8'))
            
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
        auth = 0
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
