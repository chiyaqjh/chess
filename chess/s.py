import socket
import threading

SERVER = '10.151.24.239'
PORT = 6689
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []

def broadcast(message):
    for client in clients:
        client.send(message.encode(FORMAT))

def handle(client):
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            print(msg)
            broadcast(msg)
        except:
            clients.remove(client)
            client.close()
            break

def start():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, _ = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()

print("Starting server...")
start()
