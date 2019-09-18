import socket
from threading import Thread

clients = set()
#Add a feature that imports the dict from a file, make it do ports to so you can have multiple running on one computer
filee = open('ips.txt','r')
ips = eval(filee.read())


def ipDecode():
    ips

def broadcast(clients,data):
    for c in clients:
        print(c)
        c.send(data)
        #print('hey')

class Client(Thread):

    def __innit__(self,ip,port,buffer):
        Thread.__innit__(self)
        self.ip = ip
        self.port = port
        self.buffer = buffer
        print ('New connection from ', ip)

    def run(self):
        while True:
            data = conn.recv(buffer)
            
            if ip in ips:
                print(ip+data.decode('utf-8'))
                pass
            else:
                ips[ip] = data.decode('utf-8')

            
            fullmessage = ips[ip]+': '
            fullmessage = fullmessage.encode('utf-8')
            fullmessage+= data
            
            print(fullmessage.decode('utf-8'))
            broadcast(clients, fullmessage)
            #message = input('Enter message: ')
            #if message == 'exit':
            #    break
            #conn.send(message.encode())
            

tcp_ip = '0.0.0.0'
tcp_port = 9898
buffer = 1024
newthread={}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((tcp_ip,tcp_port))

while True:
    server.listen(9)
    (conn, (ip,port)) = server.accept()
    clients.add(conn)
    newthread[ip] = Client(None,ip,port,buffer)
    newthread[ip].start()
