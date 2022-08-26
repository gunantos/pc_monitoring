from ast import parse
import asyncio
import json
import os
from urllib import request
from pc_monitoring.library.pc import PC
from pc_monitoring.library.convert import UnitByte
from pc_monitoring.my_socket import MySocket


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


class PC(__Monit):
    @property
    def info(self):
        return {
            "os": self.pc.os,
            "hostname": self.pc.hostname,
            "architecture": self.pc.architecture,
            "mac_address": self.nif.mac_address,
            "ip_address": self.nif.ip_address,
            "gateway": self.nif.gateway}

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

    def get(self, exclude=[]):
        method_list = [method for method in dir(
            self) if method.startswith('__') is False]
        hasil = {}
        for x in method_list:
            x = x.lower()
            if x not in exclude:
                print(x)
                hasil[x] = self[x]
        return hasil

    def toJSON(self, data):
        return bytes(json.dumps(data), encoding="utf-8")

    def send_info(self, API_URL, headers={}):
        if API_URL == None:
            return
        else:
            request.post(API_URL, data=self.info, headers=headers)


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
        _pc = PC()
        _sock = MySocket(self.HOST, self.PORT, self.INTERVAL)
        _data = _pc.get()
        _dataJSON = _pc.toJSON(_data)
        _sock.setData(_dataJSON)
        try:
            loop = asyncio.get_event_loop()
            asyncio.ensure_future(_sock.conn())
            loop.run_forever()
            loop.close()
        except (KeyboardInterrupt, SystemExit):
            os.exit(0)


__all__ = ['Monitoring']
