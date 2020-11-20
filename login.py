import client2
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import messagebox

def start():
    screen=Tk()
    screen.title("Connect to server")
    screen.geometry("300x250")

    global host_input
    global port_input
    global host_entry
    global port_entry
    host_input = StringVar()
    port_input = StringVar()

    Label(screen, text="Please enter details below").pack()
    Label(screen, text="").pack()
    Label(screen, text="Host * ").pack()
    host_entry = Entry(screen, textvariable=host_input)
    host_entry.pack()
    Label(screen, text="Port * ").pack()
    port_entry = Entry(screen, textvariable=port_input)
    port_entry.pack()
    Label(screen, text="").pack()
    Button(screen, text="Connect", width=10, height=1, command=None).pack()


client=client2.Client()
global screen
screen = Tk()
screen.geometry("300x250")
screen.title("404-Name Not Found")
Label(text="Chat room 1.0", bg="grey", width="300", height="2", font=("Calibri", 13)).pack()
Label(text="").pack()
Button(text="Start", height="2", width="30", command=(lambda:start())).pack()
Label(text="").pack()
screen.mainloop()


