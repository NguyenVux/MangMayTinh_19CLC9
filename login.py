import socket
import threading
import json
from tkinter import messagebox
from tkinter import *

class Client:
    def connect_server(self):
        global host
        global port
        host = host_entry.get()
        port = port_entry.get()
        if not host or not port:
            messagebox.showinfo("Warning!", "Do not empty!")
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.s.connect((host, port))
            except:
                messagebox.showerror("ERROR","Can't connect to "+host+"!")
            else:
                messagebox.showinfo("Connection status", "Connected to "+ host)
    def login_register(self):
        global username
        global screen
        action = ""
        result = dict(result="failed")
        while result["result"] != "succeed":
            screen.destroy()
            screen = Tk()
            screen.title("404_NAME NOT FOUND")
            screen.geometry("300x300")
            screen.iconbitmap('Image/messenger_qwt_icon.ico')
            screen.resizable(0, 0)
            label_title = Label(text="Chat room 1.0", bg="darkblue", fg="white", width="300", height="2",
                                font=("Arial", 13, "bold"))
            label_title.pack()
            label_username=Label(text="username")
            label_username.place()
            username_entry = Entry(screen,width=100, textvariable=username)
            label_username = Label(text="username")
            label_username.place()
            password_entry = Entry(screen, width=100, textvariable=password)
        #     if action == "dn":
        #         print("Login")
        #         username = input('Enter username --> ')
        #         password = input('Enter password --> ')
        #         loginJSON = json.dumps({"uuid": username, "pwd": password, "action": action})
        #         self.s.send(loginJSON.encode())
        #         result = json.loads(self.s.recv(1024).decode())
        #         if result["result"] == "succeed":
        #             print("Succeed")
        #             print("user info " + result["name"])
        #         else:
        #             print("Fail")
        #
        # if action == "dn" and result["result"] == "succeed":
        #     message_handler = threading.Thread(target=self.handle_messages, args=())
        #     message_handler.start()
        #
        #     input_handler = threading.Thread(target=self.input_handler, args=())
        #     input_handler.start()
    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def inputHandler(self):
        while 1:
            self.s.send(("["+username+"]:"+' - '+input()).encode())
    def log_in(self):
        pass
    def register(self):
        pass
#Declare
host=''
port=''
username=''
password=''
screen = Tk()
client=Client()
#create start windown
screen.title("404_NAME NOT FOUND")
screen.geometry("300x200")
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

Button(text="Connect", width=10, height=1, command=lambda: client.connect_server()).pack()


screen.mainloop()