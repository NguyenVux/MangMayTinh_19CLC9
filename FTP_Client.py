import FTP_core
import socket
import json
from tqdm import tqdm

class FTPClient:
    def __init__(self, host_name):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                host = input('Enter host name --> ')
                self.s.connect((host, 5001))
                break
            except:
                print("Couldn't connect to server")

    def get_file(self, file_name):
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
        FTP_core.get(data,"download",self.s)
        self.s.recv(1)
        print("Finish recv")


    def send_file(self, file):
        FTP_core.send(file, "download", self.s)
        self.s.recv(1)
        print("send")


if __name__ == '__main__':
    t = FTPClient("h")
    t.get_file("r.rar")