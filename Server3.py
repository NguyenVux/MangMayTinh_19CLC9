import errno
import threading
import socket
import json


class User(dict):
    def __init__(self, connection):
        dict.__init__(self)
        self.update({'connection': connection})


def authenticate(user):
    print(user)
    file = open("testdata.json")
    filejson = json.loads(file.read())
    if user["uuid"] in filejson:
        user_data = filejson[user["uuid"]]
        if user_data["pwd"] == user["pwd"]:
            user_data.pop("pwd", None)
            return user_data, True
    return {}, False


def signup(user):
    print(user)
    user_data = dict(uuid="123", pwd="321")
    return user_data, True


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
            connection, address = self.__socketServer.accept()
            authenticate_thread = threading.Thread(target=self.__login, args=(connection,))
            authenticate_thread.start()

    def __login(self, connection: socket):
        print("Client Connected")
        while True:
            try:
                msg = connection.recv(4096).decode()
                print(msg)
                msg = json.loads(msg)
                action = msg["action"]
                if action == "dk":
                    user, result = signup(connection)
                    if result:
                        authed_user = User(connection)
                        authed_user |= user
                        connection.send(json.dumps({"action": "dk", "result": "succeed"}).encode())
                        continue
                    connection.send(json.dumps({"action": "dk", "result": "failed"}).encode())
                if action == "dn":
                    user, result = authenticate(msg)
                    if result:
                        authed_user = User(connection)
                        authed_user |= user
                        self.__lstUser.append(authed_user)
                        connection.send(json.dumps({"action": "dn_s", "result": "succeed"}|user).encode())
                        break
                    connection.send(json.dumps({"action": "dn_f", "result": "failed"}).encode())
            except socket.error as error:
                if error.errno == errno.ECONNRESET:
                    print("Client disconnected")
                    break


s = Server()
s.start_server()