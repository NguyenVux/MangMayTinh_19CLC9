import socket
import threading
import json
class Client:
    def __init__(self):
        self.create_connection()
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host,port))
                break
            except:
                print("Couldn't connect to server")
        action = ""
        result = dict(result="failed")
        session_id = self.s.recv(1024).decode()
        while result["result"]:
            action = input('Choose what you want-> ')
            if action == "login":
                print("Login")
                username = input('Enter username --> ')
                password = input('Enter password --> ')
                loginJSON = json.dumps({"uuid": username, "pwd":password, "action":action,"session_id": session_id})
                self.s.send(loginJSON.encode())
                result = json.loads(self.s.recv(1024).decode())
                print(result)
                if result["result"]:
                    print("Succeed")
                    print("user info " + result["name"])
                    break
                else:
                    print("Fail")


        if action == "login" and result["result"]:
            message_handler = threading.Thread(target=self.handle_messages, args=(session_id,))
            message_handler.start()

            input_handler = threading.Thread(target=self.input_handler, args=(session_id,))
            input_handler.start()

    def handle_messages(self,session_id):
        while 1:
            msg = self.s.recv(1204).decode()
            msg = json.loads(msg)
            if msg["action"] == "send_msg":
                print(msg["msg"])

    def input_handler(self, session_id):
        while 1:
            action = input("action: ")
            if action == "join_room":
                print("room")
                username = input('room-> ')
                loginJSON = json.dumps({"room": username, "action": action, "session_id": session_id})
                self.s.send(loginJSON.encode())
            action = input("action: ")
            if action == "send_msg":
                print("room")
                username = input('msg-> ')
                loginJSON = json.dumps({"msg": username, "action": action, "session_id": session_id})
                self.s.send(loginJSON.encode())

client = Client()
