import socket
from threading import Thread

def receive():
    '''Recives da message'''
    while True:
        #data is what the server sends
        data = socket.recv(buffer).decode('utf-8')
        data = data.split(',')
        if data[1] == 'askinput':
            print(data[0])
            send()
        elif data[1] == 'event':
            if data[0] == 'waiting4players':
                print('Waiting...') #Waiting screen
            elif data[0] == '4players':
                print('Game start!') #Start game

def send(event=None):  # event is passed by binders.
    '''Handles sending of messages.'''
    message = input('Message to send: ')
    socket.send(bytes(message, 'utf8'))
    if message == '/quit':
        socket.close()

def on_closing(event=None):
    my_message.set('/quit')
    send()

host = '192.168.0.126'#input('Enter host: ')
port = 9899#int(input('Enter port: '))

hand = []

buffer = 2048
address = (host, port)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
