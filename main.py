import json
from monitoring import Monitoring
import asyncio
import requests
import time
import socket

API_URL = "http://192.168.243:3030"
API_KEY = "xxx"
INTERVAL_DEFAULT = 1
HOST = "0.0.0.0"
PORT = 65432
INTERVAL = INTERVAL_DEFAULT


def send_info(self):
    if self.API_URL == None:
        return
    else:
        headers = {
            "Content-type": "application/json",
            "Accept": "*",
            "X-TTPG-KEY": self.API_KEY}
        requests.post(self.API_URL, data={
            "os": self.get.general.os,
            "hostname": self.get.general.hostname,
            "architecture": self.get.general.architecture,
            "mac_address": self.get.network.mac_address,
            "ip_address": self.get.network.ip_address,
            "gateway": self.get.network.gateway}, headers=headers)


async def getData():
    cls = Monitoring()
    return {
        "info": cls.general_info,
        "cpu": cls.cpu,
        "disk": cls.disk,
        "network": cls.network
    }


def toJSON(data):
    return bytes(json.dumps(data), encoding="utf-8")


async def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                data = await getData()
                conn.sendall(toJSON({"monitoring": data}))
                time.sleep(INTERVAL)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    loop.run_forever()
    loop.close()
