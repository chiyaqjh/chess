import socket
r = socket.gethostbyname(socket.gethostname())
print(r)

import requests
r = requests.get('http://myip.ipip.net', timeout=6).text
print(r)