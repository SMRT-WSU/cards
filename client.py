import socket
from threading import Thread

ip = socket.gethostname()
port = 9898
buffer = 2048

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip,port))

class Listen(Thread):

    def __innit__(self,ip,port,buffer):
        Thread.innit(self)
        self.ip = ip
        self.pot = port
        self.buffer = buffer
        print ('New connection from ', ip)

    def run(self):
        data = client.recv(buffer)
        print (data.decode('utf-8'))

message = input('Enter message: ')
while message != 'exit':
    newthread = Listen(None,ip,port,buffer)
    client.send(message.encode('utf-8'))
    message = input('Enter message: ')

client.close()