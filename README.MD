## MONITORING COMPUTER WITH SOCKET
![Python Logo](https://www.python.org/static/community_logos/python-logo.png "Sample inline image")

Aplikasi monitoring ini mengunakan socket yang akan mengirim data informasi computer ke server

### Install
this project is testing release
```cmd
pip install -i https://test.pypi.org/simple/ pc_monitoring
```

### Using Library
- COMPUTER
```python
from pc_monitoring.monitoring import Monitoring
CLS = Monitoring()
#or set spesific HOST, PORT, INTERVAL
# PORT default 65432
# CLS = Monitoring('127.0.0.1', 65432, 1) 
cls.run()
#or if you using async 
# await cls.run_async()
```

- SERVER OR RECIVE DATA
create socket client connection
```python
import json
import socket

HOST = '127.0.0.1'
PORT = 65432

def toJSON(data):
    return bytes(json.dumps(data), encoding="utf-8")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(toJSON({"test": "Test"}))
    data = s.recv(1024)

print(data)
```

### Install
- Windows
    download latest release and install
    
- Linux