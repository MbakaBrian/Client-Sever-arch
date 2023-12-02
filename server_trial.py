import socket
import threading
import jwt # PyJWT library
import datetime

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECTED FROM SERVER"
SECRET_KEY = 'Brian'  # Replace with a strong secret key

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

def generate_token():
    # Generate a JWT token with an expiration time (e.g., 1 hour)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {'exp': expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        # Verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Invalid token
        return False

def handle_client(conn, addr):
    print(f"[New Connection] {addr} connected")
    connected = True

    # Generate a JWT token for the client
    token = generate_token()
    conn.send(token.encode(FORMAT))

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # Verify the received JWT token
            if verify_token(msg):
                print(f"[{addr}] {msg}")
            else:
                print(f"[{addr}] Unauthorized access detected. Disconnecting...")
                connected = False

    conn.close()

def start():
    server.listen()
    print("Server is listening...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("Starting server....")
print(f"Your address is {SERVER}")
start()
