from database import DataBase
import errno
import threading
import socket
import json
import random
import FTP_Server

class User(dict):
    def __init__(self, connection):
        dict.__init__(self)
        self.update({'connection': connection})


def authenticate(user, db: DataBase):
    query = {"uuid": user["uuid"]}
    result = db.user_db.find(query, {"_id": 0})
    for r in result:
        if r["pwd"] == user["pwd"]:
            r.pop("pwd", None)
            return r, True
    # if user["uuid"] in file_json:
    #     user_data = file_json[user["uuid"]]
    #     if user_data["pwd"] == user["pwd"]:
    #         user_data.pop("pwd", None)
    #         return user_data, True
    return {}, False


def signup(user, db: DataBase):
    query = {"uuid": user["uuid"]}
    result = db.user_db.find(query, {"_id": 0})
    if result.count() == 0 and "uuid" in user and "pwd" in user:
        data = \
            {
                "uuid": user["uuid"],
                "pwd": user["pwd"],
                "name": "",
                "dob": ""
            }
        db.user_db.insert_one(data)
    return {"errmsg": "user name is exist or missing request info"}, False


def gen_id(exist_lst, max_id):
    session_id = random.randint(0, max_id)
    while session_id in exist_lst:
        session_id = random.randint(0, max_id)
    return str(session_id)


class Server:
    def __init__(self, db_object: DataBase):
        self.ftp_server = object
        self.__socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__lstUser = list()
        self.__lstSession = dict()
        self.__dictAction = dict()
        self.__dictAction["login"] = self.__login
        self.__dictAction["send_msg"] = self.__send_msg
        self.__dictAction["register"] = self.__register
        self.__dbObject = db_object

        self.__dictRoom = dict()

    def start_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 5000 #int(input('Enter port to run the server on --> '))
        self.ftp_server = FTP_Server.FTPServer(port +1)
        self.__socketServer.bind((host, port))
        self.__socketServer.listen(100)
        print('Starting MSG server:')
        print('Running on host: ' + str(host))
        print('Running on port: ' + str(port))
        while True:
            connection, address = self.__socketServer.accept()
            self.__init_session(connection)

    def __init_session(self, connection: socket):
        user = User(connection)
        session_id = gen_id(self.__lstSession, 100)
        self.__lstSession.update({session_id: user})
        connection.send(session_id.encode())
        threading.Thread(target=self.__session_loop, args=(session_id,)).start()

    def __session_loop(self, session_id: str):
        session = self.__lstSession[session_id]
        print("Client Connected")
        while True:
            try:
                msg = session["connection"].recv(1024).decode()
                msg = json.loads(msg)
                if msg["session_id"] == session_id:
                    self.__dictAction[msg["action"]](msg, session_id)
            except socket.error as error:
                if error.errno == errno.ECONNRESET:
                    self.__lstSession.pop(session_id, None)
                    print("Client disconnected")
                    break
        self.__notify_status(session_id)
        print(self.__lstSession.keys())

    def __login(self, json_data: dict, session_id):
        if not self.__login_check(session_id):
            session = self.__lstSession[session_id]
            if "uuid" in json_data and "pwd" in json_data:
                data, result = authenticate(json_data, self.__dbObject)
                response = dict(action=json_data["action"])
                response |= data
                response |= {"result": result}
                session["connection"].send(json.dumps(response).encode())
                response.pop("action")
                response.pop("result")
                session |= response
                if result:
                    self.__notify_status(session_id)
                print(session)

    def __send_msg(self, json_data: dict, session_id):
        session = self.__lstSession[session_id]
        if self.__login_check(session_id):
            print("message by [" + session["name"] + "]" + "\n" + json_data["msg"])
            for i in self.__lstSession:
                self.__lstSession[i]["connection"].send(
                    json.dumps(
                        {"result": True, "action": "send_msg",
                         "msg":json_data["msg"],
                         "sender": session["name"]
                         }).encode())

    def __register(self, json_data: dict, session_id):
        session = self.__lstSession[session_id]
        if self.__login_check(session_id):
            session["connection"].send(json.dumps({"action": json_data["action"],
                                                   "result": False,
                                                   "errmsg": "already logged in"
                                                   }).encode())
        else:
            data, result = signup(json_data)
            data |= {"result": result,
                     'action': json_data["action"]}
            session["connection"].send(json.dumps(data).encode())

    def __login_check(self, session_id):
        session = self.__lstSession[session_id]
        response = session.copy()
        response.pop("connection")
        return bool(response)

    def __notify_status(self, session_id):
        data = {"action": "status_notify", "user_list": []}
        for u in self.__lstSession:
            data["user_list"].append(self.__lstSession[u]["name"])
        for u in self.__lstSession:
            data["user_list"].remove(self.__lstSession[u]["name"])
            self.__lstSession[u]["connection"].send(json.dumps(data).encode())
            data["user_list"].append(self.__lstSession[u]["name"])


try:
    db = DataBase()
    s = Server(db)
    s.start_server()
except socket.error as err:
    print(err)
