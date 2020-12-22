import threading
import FTP_core
import socket
import json
from PyQt5.QtCore import *
import time


class FTPClient():


    def __init__(self, host_name, port):
        self.file = FTP_core.FTPCore()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                self.s.connect((host_name, int(port)))
                break
            except:
                print("Couldn't connect to server")

    def _get_file(self, json_data, root):
        self.file.get(json_data, root, self.s)
        self.s.recv(1)
        print("Finish recv")

    def get_file(self, file_name, root="upload"):
        header = FTP_core.Header()
        header.action = FTP_core.GET
        header.file_name = file_name
        header.length = 0
        self.s.send(header.to_json_str().encode())

        data = b""
        while b"\r\n\r\n" not in data:
            data += self.s.recv(1)
        data = data.decode()
        print(data)
        data = json.loads(data)
        threading.Thread(target=self._get_file, args=(data, root,))

    def _send_file(self, file, root, callback=None):
        self.file.send(file, root, self.s, callback)
        self.s.recv(1)
        print("send")

    def send_file(self, file, root, bar):
        ts = threading.Thread(target=self._send_file, args=(file, root,))
        ts.start()
        while ts.is_alive():
            if self.file.ready:
                value = self.file.byte * 100 / self.file.length
                bar.emit(value)
        time.sleep(5)
        bar.emit(0)
    def __del__(self):
        print("finish upload/download")


if __name__ == '__main__':
    t = FTPClient("h")
    t.get_file("readme.txt")
    t = FTPClient("h")
    t.send_file("r.rar")
