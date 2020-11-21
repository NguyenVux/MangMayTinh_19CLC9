import socket
import threading
import json
class Client:
    def create_connection(self,host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while 1:
            try:
                self.s.connect((host,port))
                break
            except:
                return False
        action = ""
        result = dict(result="failed")
        while result["result"] != "succeed":
            action = input('Choose what you want')
            if action == "dn":
                print("Login")
                username = input('Enter username --> ')
                password = input('Enter password --> ')
                loginJSON = json.dumps({"uuid": username, "pwd":password, "action":action})
                self.s.send(loginJSON.encode())
                result = json.loads(self.s.recv(1024).decode())
                if result["result"] == "succeed":
                    print("Succeed")
                    print("user info " + result["name"])
                else:
                    print("Fail")

        if action == "dn" and result["result"] == "succeed":
            message_handler = threading.Thread(target=self.handle_messages, args=())
            message_handler.start()

            input_handler = threading.Thread(target=self.input_handler, args=())
            input_handler.start()

    def handle_messages(self):
        while 1:
            print(self.s.recv(1204).decode())

    def input_handler(self):
        while 1:
            self.s.send(("["+self.username+"]:"+' - '+input()).encode())

