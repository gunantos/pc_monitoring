import socket
import time
from _thread import *


class MySocket():
    def __init__(self, HOST=None, PORT=None, INTERVAL=1):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERVAL = INTERVAL * 60
        if self.HOST == None:
            self.HOST = ''
        if self.PORT == None:
            self.PORT = 65432

    def setData(self, data):
        self.DataSend = data

    async def conn(self):
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((self.HOST, self.PORT))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {self.PORT}')
        ServerSocket.listen()
        while True:
            self.accept_connections(ServerSocket)

    def accept_connections(self, ServerSocket):
        Client, address = ServerSocket.accept()
        print(f'Connected to: {address[0]}:{str(address[1])}')
        start_new_thread(self.client_handler, (Client, ))

    async def broadcast(self, connection):
        try:
            connection.sendall(str.encode(self.DataSend))
        except connection:
            print('Terjadi kesalahan dalam pengiriman data')

    def getDataClient(self, connection):
        data = connection.recv(2048).decode('utf-8')
        parse_data = json.loads(data)
        interval = parse_data.get('interval', 0)
        stop = parse_data.get('stop', True)
        if interval > 0:
            self.INTERVAL = int(interval) * 60
            self.RUN = stop

    def client_handler(self, connection):
        connection.send(str.encode(
            'You are now connected to the replay server...'))
        while self.RUN:
            self.getDataClient(connection)
            self.broadcast(connection)
            time.sleep(self.INTERVAL)
        connection.close()


__all__ = ['MySocket']
