import copy
import errno
import threading
import socket
import json
import random

class User(dict):
    def __init__(self, connection):
        dict.__init__(self)
        self.update({'connection': connection})


def authenticate(user):
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

    def notify(self, mess: str, user) -> None:
        print("message by: " + mess)
        if user in self.__lstUser:
            for i in self.__lstUser:
                if i is not user:
                        i["connection"].send(json.dumps({"result": True, "action": "send_msg", "msg": i["name"]+": " + mess}))
            return
        user["connection"].send(json.dumps({"result": False, "action": "send_msg"}).encode())

    def subscribe(self, user) -> bool:
        if not(user in self.__lstUser):
            self.__lstUser.append(user)
            return True
        return False

    def unsubscribe(self, user: dict) -> None:
        self.__lstUser.append(user)


def gen_id(exist_lst, max_id):
    session_id = random.randint(0, max_id)
    while session_id in exist_lst:
        session_id = random.randint(0, max_id)
    return str(session_id)


class Server:
    def __init__(self):
        self.__socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__lstUser = list()
        self.__lstSession = dict()
        self.__dictAction = dict()
        self.__dictAction["login"] = self.__login
        self.__dictAction["join_room"] = self.__join_room
        self.__dictAction["send_msg"] = self.__send_msg
        self.__dictRoom = dict()

    def start_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter port to run the server on --> '))

        self.__socketServer.bind((host, port))
        self.__socketServer.listen(100)
        print('Running on host: ' + str(host))
        print('Running on port: ' + str(port))
        while True:
            connection, address = self.__socketServer.accept()
            self.__init_session(connection)

    def __init_session(self, connection: socket):
        user = User(connection)
        session_id = gen_id(self.__lstSession, 100)
        self.__lstSession.update({session_id: user})
        connection.send(session_id.endcode())
        threading.Thread(target=self.__session_loop, args=(session_id,)).start()

    def __session_loop(self, session_id: str):
        session = self.__lstSession[session_id]
        print("Client Connected")
        while True:
            try:
                msg = session["connection"].recv(4096).decode()
                try:
                    msg = json.loads(msg)
                    if msg["session_id"] == session_id:
                        self.__dictAction[msg["action"]](msg, session_id)
                except:
                    continue
            except socket.error as error:
                if error.errno == errno.ECONNRESET:
                    self.__lstSession.pop(session_id, None)
                    print("Client disconnected")
                    break
        print(self.__lstSession.keys())

    def __join_room(self, json_data: dict, session_id):
        if self.__login_check(session_id):
            if not (json_data["room"] in self.__dictRoom):
                self.__dictRoom.update({json_data["room"]: Room()})
            result = self.__dictRoom[json_data["room"]].subscribe(self.__lstSession[session_id])
            self.__lstSession[session_id]["connection"].send(json.dumps({"result": result, "action": "join_room"}).encode())

    def __login(self, json_data: dict, session_id):
        if not self.__login_check(session_id):
            session = self.__lstSession[session_id]
            if "uuid" in json_data and "pwd" in json_data:
                data, result = authenticate(json_data)
                response = dict(action=json_data["action"])
                response |= data
                response |= {"result": result}
                session["connection"].send(json.dumps(response).encode())
                response.pop("action")
                response.pop("result")
                session |= response

    def __send_msg(self, json_data: dict, session_id):
        if self.__login_check(session_id):
            session = self.__lstSession[session_id]
            self.__dictRoom[session["room"]].notify(json_data["msg"], session)

    def __login_check(self, session_id):
        session = self.__lstSession[session_id]
        response = session.copy()
        response.pop("connection")
        return bool(response)

s = Server()
s.start_server()
