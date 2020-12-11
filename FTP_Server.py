import FTP_core
import socket
import threading
import errno
import json


class FTPServer:
    timeout_seconds = 3000

    def __init__(self, port):
        self.FTP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        self.FTP_socket.bind((host, port))
        print('Running on host: ' + str(host))
        print('Running on port: ' + str(port))
        self.FTP_socket.listen(100)
        #self.FTP_socket.settimeout(self.timeout_seconds)
        while True:
            connection, address = self.FTP_socket.accept()
            threading.Thread(target=self.__handle_connection, args=(connection,)).start()

    @staticmethod
    def __handle_connection(connection):
        try:
            data = b""
            while b"\r\n\r\n" not in data:
                data += connection.recv(1)
            data = data.decode()
            data = json.loads(data)
            if data['action'] == FTP_core.GET:
                FTP_core.send(data["file_name"], "upload", connection)
            if data['action'] == FTP_core.SEND:
                FTP_core.get(data, "upload", connection)
            connection.send(b'1')
            connection.close()
        except socket.error as err:
            if err.errno == errno.ECONNRESET:
                print("Client disconnected")



if __name__ == '__main__':
    t = FTPServer(5001)