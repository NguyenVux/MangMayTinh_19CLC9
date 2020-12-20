from database import DataBase
import errno
import threading
import socket
import json
import random
import FTP_Server
from action_util import Action
import json_util


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
    return {}, False


def signup(user, db: DataBase):
    if "uuid" in user and "pwd" in user:
        query = {"uuid": user["uuid"]}
        if db.user_db.count_documents(query) == 0:
            data = \
                {
                    "uuid": user["uuid"],
                    "pwd": user["pwd"],
                    "name": "",
                    "dob": ""
                }
            db.user_db.insert_one(data)
            return {"errmsg": ""}, True
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
        self.__dictAction[Action.login] = self.__login
        self.__dictAction[Action.send_message] = self.__send_msg
        self.__dictAction[Action.sign_up] = self.__register
        self.__dictAction[Action.change_pwd] = self.__changepwd
        self.__dictAction[Action.update_info] = self.__update_info
        self.__dictAction[Action.view_info] = self.__view_info
        self.__dbObject = db_object

        self.__dictRoom = dict()

    def start_server(self):
        host = socket.gethostbyname(socket.gethostname())
        port = 5000  # int(input('Enter port to run the server on --> '))
        self.ftp_server = FTP_Server.FTPServer(port + 1)
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
                # msg = session["connection"].recv(1024).decode()
                msg = json_util.receive(session["connection"]).decode()
                if msg[0] == "{" and msg[-1] == "}":
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
                # session["connection"].send(json.dumps(response).encode())
                json_util.send(json.dumps(response), session["connection"])
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
            if "private_list" not in json_data or not json_data["private_list"]:
                for i in self.__lstSession:
                    # self.__lstSession[i]["connection"].send(
                    #     json.dumps(
                    #         {"result": True, "action": "send_msg",
                    #          "msg":json_data["msg"],
                    #          "sender": session["name"]
                    #          }).encode())
                    json_util.send(
                        json.dumps(
                            {"result": True, "action": Action.send_message,
                             "msg": json_data["msg"], "private": 0,
                             "sender": session["name"]
                             }), self.__lstSession[i]["connection"])
            else:
                for i in self.__lstSession:
                    if self.__lstSession[i]["uuid"] in json_data["private_list"]:
                        json_util.send(
                            json.dumps(
                                {"result": True, "action": Action.send_message,
                                 "msg": json_data["msg"], "private": 1,
                                 "sender": session["name"]
                                 }), self.__lstSession[i]["connection"])

    def __register(self, json_data: dict, session_id):
        session = self.__lstSession[session_id]
        if self.__login_check(session_id):
            # session["connection"].send(json.dumps({"action": json_data["action"],
            #                                        "result": False,
            #                                        "errmsg": "already logged in"
            #                                        }).encode())
            json_util.send(json.dumps({"action": json_data["action"],
                                       "result": False,
                                       "errmsg": "already logged in"
                                       }), session["connection"])
        else:
            data, result = signup(json_data, self.__dbObject)
            data |= {"result": result,
                     'action': json_data["action"]}
            json_util.send(json.dumps(data), session["connection"])

    def __login_check(self, session_id):
        session = self.__lstSession[session_id]
        response = session.copy()
        response.pop("connection")
        return bool(response)

    def __notify_status(self, session_id):
        key = "uuid"
        data = {"action": Action.status_notify, "user_list": []}
        for u in self.__lstSession:
            if "name" in self.__lstSession[u]:
                data["user_list"].append(self.__lstSession[u][key])
        for u in self.__lstSession:
            if "name" in self.__lstSession[u]:
                data["user_list"].remove(self.__lstSession[u][key])
                json_util.send(json.dumps(data), self.__lstSession[u]["connection"])
                data["user_list"].append(self.__lstSession[u][key])

    def __changepwd(self, json_data, session_id):
        session = self.__lstSession[session_id]
        print(json_data)
        if not self.__login_check(session_id):
            json_util.send(json.dumps({"action": json_data["action"],
                                       "result": False,
                                       "errmsg": "not logged in"
                                       }), session["connection"])
        else:
            json_data |= {"uuid": session["uuid"]}
            data, result = authenticate(json_data, self.__dbObject)
            print(result)
            if result:
                self.__dbObject.user_db.update_one({"uuid": session["uuid"]},
                                                   {'$set': {
                                                       "pwd": json_data['new_pwd']
                                                   }
                                                   })
            json_util.send(json.dumps({"result": result,
                                       "action": json_data["action"]
                                       }), session["connection"])

    def __update_info(self, json_data, session_id):
        session = self.__lstSession[session_id]
        if self.__login_check(session_id):
            query = {"uuid": session["uuid"]}
            new_info = {"name": json_data["name"],
                        "dob": json_data["dob"],
                        "email": json_data['email']
                        }
            self.__dbObject.user_db.update(query, {"$set": new_info})

    def __view_info(self,json_data, session_id):
        session = self.__lstSession[session_id]
        if self.__login_check(session_id):
            query = {"uuid": json_data["uuid"]}
            result = self.__dbObject.user_db.find_one(query, {"_id": 0, "pwd": 0})
            for r in result:
                data = r
                data |= {"result": True,
                         "action": json_data["action"]}
                json_util.send(json.dumps(data),
                               session["connection"])
                return
            data = {"result": False,
                    "action": json_data["action"]}
            json_util.send(json.dumps(data),
                       session["connection"])
try:
    db = DataBase()
    s = Server(db)
    s.start_server()
except socket.error as err:
    print(err)
