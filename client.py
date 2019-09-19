import tkinter
import socket
from threading import Thread

def colour(data):
    colours = {
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
            font = colour(data[0:2])
            splitdata = data.split(':')
            if len(splitdata) == 2:
                user = splitdata[0][2:]+': '
                message = splitdata[1]+'\n'
            else: # System message
                user = data[2:]
            try: #see if its a system message
                message = splitdata[1]+'\n'
            except:
                pass

            line = int(message_list.index('end-1c').split('.')[0])
            print(line)
            message_list.tag_config('user', foreground=font)
            message_list.insert(tkinter.END, user)
            if font == 'gray':
                message_list.tag_add('user', str(line+.0), str(line)+'.'+str(len(user)))
            else:
                message_list.tag_add('user', str(line+.0), str(line)+'.'+str(len(user)))
            try:
                message_list.insert(tkinter.END, message)
                message_list.config(state=DISABLED)
            except: # Should check what kind of error i expect (to improve this)
                pass
        except OSError:  # Don't know why, but if this aint here, it sometimes breaks
            break


def send(event=None):  # event is passed by binders.
    '''Handles sending of messages.'''
    message = my_message.get()
    my_message.set('')  # Clears input field.
    socket.send(bytes(message, 'utf8'))
    if message == '/quit':
        socket.close()
        canvas.destroy()


def on_closing(event=None):
    my_message.set('/quit')
    send()

canvas = tkinter.Tk()
canvas.title('CAB')

messages_frame = tkinter.Frame(canvas)
my_message = tkinter.StringVar()  
#my_message.set('')
scrollbar = tkinter.Scrollbar(messages_frame)
message_list = tkinter.Text(messages_frame, height=15, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(canvas, textvariable=my_message)
entry_field.bind('<Return>', send)
entry_field.pack()
send_button = tkinter.Button(canvas, text='Send', command=send)
send_button.pack()

canvas.protocol('WM_DELETE_WINDOW', on_closing)

host = '192.168.1.140'#input('Enter host: ')
port = 9898#int(input('Enter port: '))


buffer = 2048
address = (host, port)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(address)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
