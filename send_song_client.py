import socket
from AES import *
from KeyGenerator import *
import pickle
import os

KEY = os.urandom(16)
print KEY


class Client(object):
    """ creating client """
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 4500))
        self.aes = AESCrypt()
        self.rsa = Cryptonew()
        self.public = ''

    def unpack(self, data):
        return pickle.loads(data.decode('base64'))

    def pack(self, data):
        return pickle.dumps(data).encode('base64')


def main():
    client = Client()
    client.public = client.client_socket.recv(1024)
    client.public = client.unpack(client.public)
    encrypted_key = client.rsa.encrypt(KEY, client.public)
    client.client_socket.send(encrypted_key)
    p = client.client_socket.recv(1024)
    while True:
        name = raw_input()
        name = client.aes.AddPadding(name)
        encryptd_message = client.aes.encryptAES(KEY, name)
        client.client_socket.send(encryptd_message)
        response = client.client_socket.recv(1024)
        response = client.aes.decryptAES(KEY, response)
        response = client.aes.StripPadding(response)
        print response


if __name__ == '__main__':
    main()