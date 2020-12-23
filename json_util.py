import socket
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

open_delimiter = b"$-{"
ending_delimiter = b"}-$"


password_provided = "password"  # This is input in the form of a string
password = password_provided.encode()  # Convert to type bytes
salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))

def receive(sock: socket):
    f = Fernet(key)
    data = b''
    i = 10
    while not (data.startswith(open_delimiter) and data.endswith(ending_delimiter)):
        data += sock.recv(1)
    return f.decrypt(data[2:-2])


def send(json_data, sock: socket):
    f = Fernet(key)
    json_data = json_data[1:-1]
    json_data = open_delimiter + f.encrypt(json_data.encode()) + ending_delimiter
    sock.send(json_data)
