import tkinter
import socket
from threading import Thread
from ast import literal_eval
from win10toast import ToastNotifier
import ctypes
import os

def colour(data):
    colours = {
            'CO':'',
            '!!':'deep pink',
            '99':'',
            '00':'grey',
            '01':'cyan',
            '02':'deep sky blue',
            '03':'indian red',
            '04':'OliveDrab1',
            '05':'SpringGreen2',
            '06':'HotPink3',
            '07':'DarkOrange1',
            '08':'DarkOrchid3',
            '09':'VioletRed2',
            '10':'MediumPurple1',
            '11':'SeaGreen2',
            '12':'blue violet',
            '13':'firebrick3',
            '14':'cornflowerblue',
            '15':'navajo white',
            '16':'lawn green',
            '17':'saddle brown',
            '18':'coral',
            '19':'forest green',
            '20':'misty rose'
        }
    print (data)
    colour = colours[data]
    return colour

def receive():
    '''Recives da message'''
    while True:
        try:
            data = socket.recv(buffer).decode('utf-8')
            try:
                font = colour(data[0:2])
            except KeyError: #For super long terminal responses that exceed my buffer
                data = 'CO'+data
            splitdata = data.split(':')
            print(data)

            if len(splitdata) >= 2:
                user = splitdata[0][2:]+': '
                message = ':'.join(splitdata[1:])+'\n'
            else: # System message
                user = data[2:]
                message = ''

            try: #see if its a system message
                message = splitdata[1]+'\n'
            except:
                pass

            fontsize = ('verdana')
            line = int(message_list.index('end-1c').split('.')[0])
            print(line)
            message_list.config(state='normal')

            if data[:2] == 'CO':
                message_list.insert(tkinter.END, data[2:])
            else:
                if data[:2] == '!!':
                    toaster.show_toast('Notification from CAB', user, icon_path='./data/icon.ico', duration=5, threaded=True)
                    fontsize = ('System', 30, 'bold')
                    ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True )
                if data[:2] == '99':
                    fontsize = ('Courier', 10)
                message_list.tag_config(font, foreground=font, font=fontsize)
                message_list.insert(tkinter.END, user)
                message_list.tag_add(font, str(line+.0), str(line)+'.'+str(len(user)))
                try:
                    message_list.tag_config(message, foreground=font, font=fontsize)
                    message_list.insert(tkinter.END, message)
                    message_list.tag_add(message, str(line) +'.'+str(len(user)), str(line)+'.'+str(len(user)+len(message)))
                except: # Should check what kind of error i expect (to improve this)
                    pass
            message_list.config(state='disabled')
            message_list.see('end')
        except OSError:  # Don't know why, but if this aint here, it sometimes breaks
            break


def send(event=None):  # event is passed by binders.
    '''Handles sending of messages.'''
    message = my_message.get()
    my_message.set('')  # Clears input field.
    try:
        socket.send(bytes(message, 'utf-8'))
    except ConnectionResetError:
        pass

    if message == '/pwd':
        message = 'Your current directory is '+os.getcwd()+'\n'
        lines = int(message_list.index('end-1c').split('.')[0])
        print(lines)
        fontsize = ('Courier', 10)
        message_list.config(state='normal')
        message_list.tag_config('hi', font=fontsize)
        message_list.insert(tkinter.END, message)
        message_list.tag_add('hi', str(lines+.0), str(lines)+'.'+str(len(message)))
        message_list.config(state='disabled')
        message_list.see('end')

    hello = message.split(' ')
    if hello[0] == '/upload':
        print('hello')
        
        try:
            p=0
            print('len'+str(len(hello)))
            for i in range(len(hello)-1):
                if hello[i] == '-n':
                    name = ' '.join(hello[i+1:])
                    print('name '+name)
                    p = i
                if hello[i] == '-p':
                    filepath = ' '.join(hello[i+1:p-2])
                    print('filepath '+filepath)
                
            f = open(filepath, 'rb')
            data = f.read()
            f.close()
            print('opened')
            padding = 64 - len(name)
            socket.send(bytes(name+padding*' ', 'utf-8'))
            print('sent filename')
            socket.send(data)
            print('sent file data')
            socket.send(bytes('AA01', 'utf-8'))
        except FileNotFoundError:
            message = 'File Not Found\n'
            lines = int(message_list.index('end-1c').split('.')[0])
            print(lines)
            fontsize = ('Courier', 10)
            user = len(message[2:])
            message_list.config(state='normal')
            message_list.tag_config('hi', font=fontsize)
            message_list.insert(tkinter.END, user)
            message_list.tag_add('hi', str(lines+.0), str(lines)+'.'+str(user))
            try:
                message_list.insert(tkinter.END, message)
            except: # Should check what kind of error I expect (to improve this)
                pass
            message_list.config(state='disabled')
            message_list.see('end')
                       
        '''except:
            message = 'Failed to upload\n'
            lines = int(message_list.index('end-1c').split('.')[0])
            print(lines)
            fontsize = ('Courier', 10)
            user = len(message[2:])
            message_list.config(state='normal')
            message_list.tag_config('hi', font=fontsize)
            message_list.insert(tkinter.END, user)
            message_list.tag_add('hi', str(lines+.0), str(lines)+'.'+str(user))
            try:
                message_list.insert(tkinter.END, message)
            except: # Should check what kind of error i expect (to improve this)
                pass
            message_list.config(state='disabled')
            message_list.see('end')'''
             
    if message == '/colour list':
         f = open('./data/colours.txt')

         data = literal_eval(f.read())
         f.close()
         for i in data:
             message = ': '+data[i]+'\n'
             font = colour(data[i])
             lines = int(message_list.index('end-1c').split('.')[0])
             print(lines)
             message_list.config(state='normal')
             user = i
             message_list.tag_config(font, foreground=font)
             message_list.insert(tkinter.END, user)
             message_list.tag_add(font, str(lines+.0), str(lines)+'.'+str(len(user)))
             try:
                 message_list.insert(tkinter.END, message)
                 message_list.config(state='disabled')
             except: # Should check what kind of error i expect (to improve this)
                 pass
             message_list.see('end')
             
    if message == '/quit':
        socket.close()
        canvas.destroy()


def on_closing(event=None):
    my_message.set('/quit')
    send()

#Add functionality for pressing the up arrow to get last message
toaster = ToastNotifier()
canvas = tkinter.Tk()
canvas.title('CAB')

messages_frame = tkinter.Frame(canvas)
my_message = tkinter.StringVar()  
#my_message.set('')
scrollbar = tkinter.Scrollbar(messages_frame)
message_list = tkinter.Text(messages_frame, height=25, width=150, state='disabled', yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(canvas, textvariable=my_message, width=100)
entry_field.bind('<Return>', send)
entry_field.pack()
entry_field.focus()
send_button = tkinter.Button(canvas, text='Send', command=send)
send_button.pack()

canvas.protocol('WM_DELETE_WINDOW', on_closing)

host = '192.168.1.179'#input('Enter host: ')
port = 9898#int(input('Enter port: '))


buffer = 8192
address = (host, port)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
