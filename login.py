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
                self.s.connect((host, int(port)))
            except:
                messagebox.showerror("ERROR","Can't connect to "+host+"!")
            else:
                messagebox.showinfo("Connection status", "Connected to "+ host)
                self.login_register()
    def login_register(self):
        global username
        global screen
        self.action = ""
        self.result = dict(result="failed")
        screen.destroy()
        screen = Tk()
        screen.title("404_NAME NOT FOUND")
        screen.geometry("400x400")
        screen.iconbitmap('Image/messenger_qwt_icon.ico')
        screen.resizable(0, 0)
        label_title = Label(text="Chat room 1.0", bg="darkblue", fg="white", width="300", height="2",
                            font=("Arial", 13, "bold"))
        label_title.pack()
        label_username=Label(text="Username", font=("Arial",10))
        label_username.place(x=77,y=85, width=100, height=20)
        self.username_entry = Entry(screen,textvariable=username)
        self.username_entry.place(x=160,y=85, width=100, height=20)
        label_username = Label(text="Password", font=("Arial",10))
        label_username.place(x=77, y=105, width=100, height=20)
        self.password_entry = Entry(screen, width=100, textvariable=password)
        self.password_entry.place(x=160,y=105, width=100, height=20)
        self.button_login = Button(text="Login", width=10, height=1, bg="darkblue", fg="white",
                              command=lambda: self.log_in())
        self.button_login.place(x=270, y=82, width=50, height=45)
        self.button_register = Button(text="Register", width=10, height=1, bg="darkblue", fg="white",
                              command=lambda: self.register())
        self.button_register.place(x=160, y=140, width=100, height=20)

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def inputHandler(self):
        while 1:
            self.s.send(("["+username+"]:"+' - '+input()).encode())
    def log_in(self):
        global username
        global password
        self.action="dn"

        username=self.username_entry.get()
        password=self.password_entry.get()
        loginJSON = json.dumps({"uuid": username, "pwd": password, "action": self.action})
        self.s.send(loginJSON.encode())

        result = json.loads(self.s.recv(1024).decode())
        if result["result"] == "succeed":
            messagebox.showinfo("Login successfully!!!!","Hello " + result["name"])
        else:
            messagebox.showerror("Fail","Username or password is incorrect or not exist")
        if self.action == "dn" and result["result"] == "succeed":

            message_handler = threading.Thread(target=self.handle_messages, args=())
            message_handler.start()

            input_handler = threading.Thread(target=self.inputHandler, args=())
            input_handler.start()


    def register(self):
        global username
        global password
        password_again=StringVar()
        Label(text="Confirm password", font=("Arial",10)).place(x=53, y=140, width=110, height=20, anchor='w')
        re_input_pass=Entry(textvariable=password_again)
        re_input_pass.place(x=160, y=130, width=100, height=20)
        self.button_register.place(x=160, y=160, width=100, height=20)

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