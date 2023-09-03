import socket
import threading
import random

# Dictionary to store clients in each room
room_clients = {}

# Function to generate a random 5-digit username
def generate_username():
    return str(random.randint(10000, 99999))

# Function to send a message to all clients in a room except the sender
def send_message_to_room(room_number, message, sender_socket):
    if room_number in room_clients:
        for client_socket, _ in room_clients[room_number]:
            if client_socket != sender_socket:
                client_socket.send(message.encode('utf-8'))

# Function to handle messages for each connected client
def handle_client(client_socket, room_number):
    username = generate_username()
    client_socket.send(username.encode('utf-8'))
    if room_number not in room_clients:
        room_clients[room_number] = []
    room_clients[room_number].append((client_socket, username))
    # print(room_clients)
   
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Room {room_number} - {username}: {message}")
            # Send the message to clients in the same room excluding the sender
            send_message_to_room(room_number, f"{username}: {message}", client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to start the server
def start_server():
    server_ip = '127.0.0.1'
    server_port = 12345
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, addr = server.accept()
        room_number = client_socket.recv(1024).decode('utf-8')
        print(f"Client connected to Room {room_number}: {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket, room_number))
        client_handler.start()

if __name__ == "__main__":
    start_server()
