import socket
import threading
import json


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096


class Client:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                host = input('Enter host name --> ')
                port = int(input('Enter port --> '))
                self.s.connect((host, port))
                break
            except:
                print("Couldn't connect to server")
        action = ""
        result = dict(result="failed")
        session_id = self.s.recv(1024).decode()
        while True:
            action = input('Choose what you want-> ')
            # login----------------------------------------------------------
            if action == "login":
                print("Login")
                username = input('Enter username --> ')
                password = input('Enter password --> ')
                loginJSON = json.dumps({"uuid": username, "pwd": password, "action": action, "session_id": session_id})
                self.s.send(loginJSON.encode())
                result = json.loads(self.s.recv(1024).decode())
                print(result)
                if result["result"]:
                    print("Succeed")
                    print("user info " + result["name"])
                    break
                else:
                    print("Fail")
            # register----------------------------------------------------------
            elif action == "register":
                print("Register")
                username = input('Enter username --> ')
                password = input('Enter password --> ')
                registerJSON = json.dumps({"uuid": username, "pwd": password, "action": action,
                                           "session_id": session_id})
                self.s.send(registerJSON.encode())
                if result["result"]:
                    print("Succeed")
                    print("user info " + result["name"])
                    name = input('Enter Name --> ')
                    dob = input('Enter Date of Birth --> ')
                    email = input('Enter Email --> ')
                    dataJSON = json.dumps({"name": name, "dob": dob, "email": email, "action": action,
                                           "session_id": session_id})
                    self.s.send(dataJSON.encode())
                    result = json.loads(self.s.recv(1024).decode())
                    print(result)
                else:
                    print("Fail")

        if action == "login" and result["result"]:
            message_handler = threading.Thread(target=self.handle_messages, args=(session_id,))
            message_handler.start()

            input_handler = threading.Thread(target=self.input_handler, args=(session_id,))
            input_handler.start()

    def handle_messages(self, session_id):
        while 1:
            msg = self.s.recv(1204).decode()
            msg = json.loads(msg)
            if msg["action"] == "status_notify":
                for i in msg["user_list"]:
                    print(i + " is online.\n")
            if msg["action"] == "send_msg":
                print(msg["sender"] + ":\t" + msg["msg"])

    def input_handler(self, session_id):
        while 1:
            action = input("action: ")
            # Stop Program-------------------------------------------------------------
            if action == "out":
                return
            # Change Password----------------------------------------------------------
            if action == "change_pwd":
                print("Old Pwd")
                old_pwd = input('msg-> ')
                print("New Pwd")
                new_pwd = input('msg-> ')
                print("New Pwd Again")
                new_pwd_2 = input('msg-> ')
                changeJSON = json.dumps({"old_pwd": old_pwd, "new_pwd": new_pwd, "new_pwd_2": new_pwd_2,
                                         "action": action, "session_id": session_id})
                self.s.send(changeJSON.encode())
                result = json.loads(self.s.recv(1024).decode())
                print(result)
            # Join Room-----------------------------------------------------------------
            if action == "join_room":
                print("room")
                username = input('room-> ')
                loginJSON = json.dumps({"room": username, "action": action, "session_id": session_id})
                self.s.send(loginJSON.encode())
            # Status Notify-----------------------------------------------------------------

            # Send Mess-----------------------------------------------------------------
            if action == "send_msg":
                print("room")
                username = input('msg-> ')
                loginJSON = json.dumps({"msg": username, "action": action, "session_id": session_id})
                self.s.send(loginJSON.encode())


# Send File-----------------------------------------------------------------
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python <check this>


client = Client()
