import socket
from threading import Thread

ip = '192.168.1.140' #socket.gethostname()
port = 9898
buffer = 2048

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('debug 1')
client.connect((ip,port))
print('debug 2')

class Listen(Thread):

    def __innit__(self,ip,port,buffer):
        Thread.innit(self)
        self.ip = ip
        self.port = port
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
