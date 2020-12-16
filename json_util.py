import socket

open_delimiter = b"$-{"
ending_delimiter = b"}-$"


def receive(sock: socket):
    data = b''
    i = 10
    while not data.startswith(open_delimiter) and not data.endswith(ending_delimiter):
        data += sock.recv(1)
    return data[2:-2]


def send(json_data, sock: socket):
    json_data = json_data[1:-1]
    json_data = open_delimiter + json_data.encode() + ending_delimiter
    sock.send(json_data)
