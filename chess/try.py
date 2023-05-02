import socket

ipv4s = socket.gethostbyname_ex(socket.gethostname())[2]

print(ipv4s[2])