import socket
import jwt  # PyJWT library
import datetime

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT = "DISCONNECTED FROM SERVER"
SERVER = "192.168.0.106"
ADDR = (SERVER, PORT)
SECRET_KEY = 'Brian'  # Replace with the same secret key used on the server side

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def generate_token():
    # Generate a JWT token with an expiration time (e.g., 1 hour)
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {'exp': expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def send_message(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Generate and send a JWT token to the server
token = generate_token()
send_message(token)

# Example messages
send_message("Hello, Server!")
send_message(DISCONNECT)
