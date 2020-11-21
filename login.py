import client2
from tkinter import messagebox
from tkinter import *

client=client2.Client()
host=''
port=''
screen = Tk()

screen.title("404_NAME NOT FOUND")
screen.geometry("300x250")
screen.iconbitmap('Image/messenger_qwt_icon.ico')
screen.resizable(0, 0)

label_title = Label(text="Chat room 1.0",bg="darkblue", fg="white", width="300", height="2", font=("Arial", 13, "bold"))
label_title.pack()

host_input = StringVar()
port_input = StringVar()

Label(text="Please enter details below").pack()
Label(text="").pack()
label_host=Label(text="Host (*)", anchor=E)
label_host.place(x=-18, y=85, width=100, height=20)
host_entry = Entry(textvariable=host_input)
host_entry.pack()
Label(text="Port (*)").place(x=9, y=105, width=100, height=20)
port_entry = Entry(textvariable=port_input)
port_entry.pack()
Label(text="").pack()

Button(text="Connect", width=10, height=1, command=lambda: connect_server()).pack()

def connect_server():
    global host
    global port
    host = host_entry.get()
    port = port_entry.get()
    if not host or not port:
        messagebox.showinfo("Warning!", "Do not empty!")
    else:
        if not client.create_connection(host, port):
            Label(text="Can't connect to " + host, fg="red")



#frame =Frame(screen, width=300, height=300)
#frame.grid(row=2, columnspan=7, sticky='WE', padx=5, pady=5, ipadx=5, ipady=5)
#frame.pack()
#screen.title("404-Name Not Found")
#label_title=Label(frame, text="Chat room 1.0", bg="darkblue", fg="white", width="300", height="2", font=("Calibri", 13))
#label_title.pack()
#Label(text="").pack()
#button_start=Button(frame, text="Start", height="2", width="30", command=lambda: start())
#button_start.pack()
#Label(text="").pack()
screen.mainloop()