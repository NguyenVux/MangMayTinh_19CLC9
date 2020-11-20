import threading
import socket
import json


class User(dict):
    def __init__(self, name: str, connection):
        dict.__init__(self)
        self.update({'connection': connection})
        self.update({'name': name})


class Room:
    def __init__(self):
        self.__lstUser = []

    def notify(self, mess: str, user: User) -> None:
        print("message by: " + mess)
        for i in self.__lstUser:
            if i is not user:
                print(i.name)

    def subscribe(self, user: User) -> None:
        self.__lstUser.append(user)


class Server:
    def __init__(self):
        self.__socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__lstUser = list()

    def start_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter port to run the server on --> '))

        self.__socketServer.bind((host, port))
        self.__socketServer.listen(100)
        print('Running on host: ' + str(host))
        print('Running on port: ' + str(port))
        while True:
            connection, addr = self.__socketServer.accept()
            authenticate_thread = threading.Thread(target=self.__authenticate, args=(connection, ))
            authenticate_thread.start()

    def __authenticate(self, connection: socket):
        msg = connection.recv(1024)
        userlogin = json.loads(msg.decode())
        if(userlogin["uuid"] == "vu" and userlogin["pwd"] == "123"):
            connection.send(True)
        else:
            connection.send(False)

s = Server()
s.start_server()