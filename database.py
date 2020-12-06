import pymongo
import json


class DataBase:
    def __init__(self):
        file = open("config.json")
        config = json.loads(file.read())
        self.client = pymongo.MongoClient(
            f'mongodb+srv://{config["user_name"]}:{config["password"]}@{config["link"]}/{config["database"]}?retryWrites'
            f'=true&w=majority')
        self.db = self.client["MANGMAYTINH"]
        self.user_db = self.db["user_db"]


# db = DataBase()
# db.user_db.insert_many([
#   {"uuid": "vu", "pwd": "123","name": "Nguyen Hoang Vu","room": 0},
#   {"uuid": "thai", "pwd": "123","name": "Nguyen Tran Hoang Thai","room": 0},
#   {"uuid": "tuan", "pwd": "123","name": "Nguyen Anh Tuan","room": 0}
# ])