import json
import socket

HOST = '192.168.1.243'
PORT = 65432


def toJSON(data):
    return bytes(json.dumps(data), encoding="utf-8")


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.connect((HOST, PORT))
ke = 0
try:
    while True:
        msg = con.recv(1024).decode('utf-8')
        print(msg)
        ke = ke + 1
        print(ke)
except (KeyboardInterrupt, SystemExit):
    exit()
except:
    exit()
