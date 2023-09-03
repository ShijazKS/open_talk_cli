import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

def connect_to_room(room_number):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))
    room_number = room_number.zfill(5)  # Ensure the room number is 5 digits
    client.send(room_number.encode('utf-8'))
    username = client.recv(1024).decode('utf-8')
    print(f"Welcome to Room {room_number}! Your username is: {username}")

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        # message = input(f"{username}: ")
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    room_number = input("Enter the room number: ")
    connect_to_room(room_number)
