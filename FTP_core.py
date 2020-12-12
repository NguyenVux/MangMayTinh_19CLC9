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
    print(header.to_dict())
    if os.path.exists(path):
        header.length = os.stat(path).st_size
        client.send(header.to_json_str().encode())
        f = open(path, "rb")
        sent = 0
        while sent < header.length:
            data = f.read(4096)
            client.send(data)
            sent += len(data)
    else:
        client.send(header.to_json_str().encode())


def get(header, root, client: socket):
    received = 0
    print(header)
    file = open(root + '/' + header["file_name"], "wb")
    while received < header["length"]:
        data = client.recv(4096)
        if len(data) > header["length"]:
            data = data[0:header["length"]]
        received += len(data)
        file.write(data)



