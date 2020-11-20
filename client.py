import socket
import threading
import json
class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host,port))
                
                break
            except:
                print("Couldn't connect to server")
        print("Login")
        username = input('Enter username --> ')
        password = input('Enter password --> ')
        loginJSON = json.dumps({"uuid":username, "pwd":password})
        self.s.send(loginJSON.encode())
        
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()

        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while 1:
            self.s.send(("["+self.username+"]:"+' - '+input()).encode())

client = Client()
