import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Client connected: {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received message: {message}")
                    self.broadcast(message, client_socket)
                else:
                    self.remove_client(client_socket)
                    break
            except Exception as e:
                print(f"Error occurred: {e}")
                self.remove_client(client_socket)
                break

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error occurred while sending message: {e}")
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            print(f"Client disconnected: {client_socket.getpeername()}")
            self.clients.remove(client_socket)
            client_socket.close()

if __name__ == '__main__':
    server = ChatServer('13.127.87.242', 1234)
    server.start()
