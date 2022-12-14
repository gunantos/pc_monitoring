from ast import parse
import asyncio
import os
import sys
from urllib import request
from library.pc import PC
from library.convert import UnitByte
from type_data import TYPEDATA
import types
import json
import socket
import time
from _thread import *


class __Monit():
    def __init__(self):
        self.pc = PC()

    def _format_bytes(self, byte_value):
        try:
            if (byte_value is None) or (byte_value == 0):
                byte_value = '0'
            elif isinstance(byte_value, (int, float)):
                val, unit = UnitByte.auto_convert(byte_value)
                byte_value = '{:.2f}'.format(val) + \
                             UnitByte.get_name_reduction(unit)
        finally:
            return byte_value

    def _transform_timetable(self, timetable, count=100):
        values = list(timetable.newest_values(count))
        keys = range(len(values))
        collection = list(zip(keys, values))
        return collection

    @property
    def disk_info(self):
        return self.pc.nonvolatile_memory

    @property
    def cpu_info(self):
        return self.pc.processor

    @property
    def mem_info(self):
        return self.pc.virtual_memory

    @property
    def nif(self):
        return self.pc.network_interface

    @property
    def current_user(self):
        return None


class Computer(__Monit):
    @property
    def info(self):
        return {
            "os": self.pc.os,
            "hostname": self.pc.hostname,
            "architecture": self.pc.architecture,
            "mac_address": self.nif.hardware_address,
            "ip_address": self.nif.ip_address,
            "gateway": self.nif.default_route}

    @property
    def general_info(self):
        total_disk_mem = 0
        for dev in self.disk_info:
            if isinstance(dev.total, (int, float)):
                total_disk_mem += dev.total
        info = {
            'os': self.pc.os,
            'architecture': self.pc.architecture,
            'hostname': self.pc.hostname,
            'cpu_name': self.cpu_info.name,
            'boot_time': self.pc.boot_time,
            'raw_uptime': int(self.pc.raw_uptime.total_seconds()),
            'uptime': self.pc.uptime,
            'total_mem': self._format_bytes(self.mem_info.total),
            'total_disk_mem': self._format_bytes(total_disk_mem)
        }
        return info

    @property
    def cpu(self):
        info = {
            'name': self.cpu_info.name,
            'count': self.cpu_info.count,
            'load': self.cpu_info.load if self.cpu_info.load else 0
        }
        return info

    @property
    def disk(self):
        info = list()
        for dev in self.disk_info:
            if dev.used_percent is None:
                used_percent = 0
            else:
                used_percent = dev.used_percent
            info.append({
                'device': dev.device,
                'mountpoint': dev.mountpoint,
                'fstype': dev.fstype,
                'used': self._format_bytes(dev.used),
                'total': self._format_bytes(dev.total),
                'used_percent': used_percent
            })
        return info

    @property
    def network(self):
        info = {
            'hostname': self.pc.hostname,
            'mac_address': self.nif.hardware_address,
            'ip_address': self.nif.ip_address,
            'mask': self.nif.subnet_mask,
            'gateway': self.nif.default_route,
            'bytes_sent': self._format_bytes(self.nif.bytes_sent),
            'bytes_recv': self._format_bytes(self.nif.bytes_recv)
        }
        return info

    async def get(self, exclude=[]):
        method_list = [method for method in dir(
            self) if method.startswith('__') is False]
        hasil = {}
        for x in method_list:
            cek = x.upper()
            if cek in TYPEDATA:
                if x not in exclude:
                    hasil[x] = getattr(self, x)
        return hasil

    def toJSON(self, data):
        return bytes(json.dumps(data), encoding="utf-8")

    def send_info(self, API_URL, headers={}):
        if API_URL == None:
            return
        else:
            request.post(API_URL, data=self.info, headers=headers)


class MySocket():
    def __init__(self, HOST=None, PORT=None, INTERVAL=1):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERVAL = INTERVAL
        self.RUN = False
        if self.HOST == None:
            self.HOST = ''
        if self.PORT == None:
            self.PORT = 65432

    def setData(self, data):
        self.DataSend = data

    async def conn(self):
        ServerSocket = socket.socket()
        self.RUN = True
        try:
            ServerSocket.bind((self.HOST, self.PORT))
        except socket.error as e:
            print(str(e))
        print(f'Server is listing on the port {self.PORT}')
        ServerSocket.listen()
        while self.RUN:
            self.accept_connections(ServerSocket)
        self.RUN = False
        ServerSocket.close()

    def accept_connections(self, ServerSocket):
        Client, address = ServerSocket.accept()
        print(f'Connected to: {address[0]}:{str(address[1])}')
        start_new_thread(self.client_handler, (Client, ))

    def broadcast(self, connection):
        try:
            connection.sendall(str.encode(self.DataSend))
        except connection:
            print('Terjadi kesalahan dalam pengiriman data')

    def getDataClient(self, connection):
        data = connection.recv(2048).decode('utf-8')
        try:
            parse_data = json.loads(data)
            interval = parse_data.get('interval', 0)
            stop = parse_data.get('stop', True)
            if interval > 0:
                self.INTERVAL = int(interval)
                self.RUN = stop
        except json.JSONDecodeError as e:
            print(e)

    async def sendAllInfo(self, connection):
        _pc = Computer()
        _data = await _pc.get()
        _dataJSON = _pc.toJSON(_data)
        connection.sendall(_dataJSON)

    def client_handler(self, connection):
        connection.send(str.encode(
            'You are now connected to the replay server...'))
        while self.RUN:
            self.getDataClient(connection)
            proc = asyncio.new_event_loop()
            asyncio.set_event_loop(proc)
            proc.run_until_complete(self.sendAllInfo(connection))
            proc.close()
            time.sleep(self.INTERVAL)
        connection.close()


class Monitoring():
    def __init__(self, HOST=None, PORT=None, INTERVAL=1):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERVAL = INTERVAL
        if self.HOST == None:
            self.HOST = ''
        if self.PORT == None:
            self.PORT = 65432

    def start(self):
        _sock = MySocket(self.HOST, self.PORT, self.INTERVAL)
        try:
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(_sock.conn())
            loop.run_forever()
            loop.close()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()
            exit()


__all__ = ['Monitoring']
