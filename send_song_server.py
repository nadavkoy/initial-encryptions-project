import threading
import socket
from AES import *
from KeyGenerator import *


class Server(object):
    def __init__(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 4500))
        self.server_socket.listen(10)
        self.rsa = Cryptonew()  # creating a new Cryptonew object to encrypt and decrypt with RSA
        self.public_key = self.rsa.get_public()  # getting the public RSA key
        self.private_key = self.rsa.get_private()  # getting the private RSA key

    def accept(self):
        return self.server_socket.accept()


class ClientHandler(threading.Thread):
    def __init__(self, address, socket, public_key, private_key, rsa):
        super(ClientHandler, self).__init__()
        self.sock = socket
        self.rsa = rsa  # rsa is a Cryptonew object that we got from server as a parameter
        self.address = address
        self.key = ''  # this variable will hold the AES that we'll get from the client
        self.public = public_key  # the public key we got from the server as a parameter
        self.private = private_key  # the private key we got from the server as a parameter
        self.aes = AESCrypt()  # creating a AESCrypt object to encrypt and decrypt with AES.

    def get_client_key(self):
        self.sock.send(self.rsa.pack(self.public))  # sending the pickled public key to the client
        encrypted_key = self.sock.recv(1024)  # getting the AES key encrypted with the public key
        self.key = self.rsa.decode(encrypted_key, self.private)  # decoding the encrypted key with the private key
        self.sock.send('gotcha')  # sends a message to the client to approve that received

    def run(self):
        self.get_client_key()
        while True:
            client_name = self.sock.recv(1024)
            client_name = self.aes.decryptAES(self.key, client_name)  # decrypt the message with AES key
            message = 'hello, ' + client_name
            message = self.aes.encryptAES(self.key, message)  # encrypt the message with AES key
            self.sock.send(message)


def main():
    server = Server()
    while True:
        socket, address = server.accept()
        client_hand = ClientHandler(address, socket, server.public_key, server.private_key, server.rsa)
        client_hand.start()


if __name__ == '__main__':
    main()

