import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECTED FORM SERVER"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT:
                connected=False
            print(f"[{addr}] {msg}")
    conn.close()
def start():
    server.listen()
    while True:
         conn,addr = server.accept()
         thread = threading.Thread(target=handle_client, args=(conn,addr))
         thread.start()
print ("Starting server....")
print (f"your address is {SERVER}")
start()