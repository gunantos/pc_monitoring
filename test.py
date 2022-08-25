import json
import socket

HOST = '192.168.1.243'
PORT = 65432


def toJSON(data):
    return bytes(json.dumps(data), encoding="utf-8")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(toJSON({"test": "Test"}))
    data = s.recv(1024)

print(data)
