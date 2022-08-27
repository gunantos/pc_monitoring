import json
import socket

HOST = '127.0.0.1'
PORT = 65432


def toJSON(data):
    return bytes(json.dumps(data), encoding="utf-8")


def fromJSON(data):
    try:
        data = json.loads(data)
        return data
    except json.JSONDecodeError as e:
        print(e)
        return data


conn = socket.socket()
conn.connect((HOST, PORT))
print(conn)
message = input(" -> ")
try:
    while True:
        conn.send(toJSON({message: message}))
        data = conn.recv(2024).decode()
        msg = fromJSON(data)
        print(msg)
    conn.close
except KeyboardInterrupt:
    print('Bye')
    exit()
