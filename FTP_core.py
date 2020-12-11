import socket
import threading
import errno
import json
import os
import tqdm

SEND = "send"
GET = "get"


class Header:

    def __int__(self):
        self.action = str
        self.length = 0
        self.file_name = str

    def to_dict(self):
        return dict(action=self.action, length=self.length, file_name=self.file_name)

    def to_json_str(self):
        return json.dumps(self.to_dict()) + "\r\n\r\n"


def send(file_name, root, client: socket):
    header = Header()
    header.action = SEND
    header.file_name = file_name
    header.length = 0
    path = root + "/" + file_name
    print(path)
    if os.path.exists(path):
        header.length = os.stat(path).st_size
        client.send(header.to_json_str().encode())
        f = open(path, "rb")
        sent = 0
        while sent < header.length:
            data = f.read(4096)
            print(data.hex())
            client.send(data)
            sent += len(data)


def get(json_data, root, client: socket):
    received = 0
    file = open(root + '/' + json_data["file_name"], "wb")
    while received < json_data["length"]:
        data = client.recv(4096)
        if len(data) > json_data["length"]:
            data = data[0:json_data["length"]]
        received += len(data)
        file.write(data)



if __name__ == '__main__':
    h = Header()
    h.action = GET
    h.length = 100
    h.file_name = "UI.py"
    path = "download/test.txt"
    h.length = os.stat(path).st_size
    print(h.to_json_str())
    #send(h.file_name)
    # print(os.path)
