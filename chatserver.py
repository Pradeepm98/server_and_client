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
        try:
            # Receive the opposite client's IP and port
            message = client_socket.recv(1024).decode('utf-8')
            opposite_ip, opposite_port = message.split(':')
            print(f"Received IP and port from opposite client: {opposite_ip}:{opposite_port}")

            # Send the client's IP and port to the opposite client
            client_ip, client_port = client_socket.getpeername()
            response = f"{client_ip}:{client_port}"
            client_socket.sendall(response.encode('utf-8'))

            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Received message: {message}")
                    self.send_to_opposite_client(message, opposite_ip, int(opposite_port))
                else:
                    self.remove_client(client_socket)
                    break
        except Exception as e:
            print(f"Error occurred: {e}")
            self.remove_client(client_socket)

    def send_to_opposite_client(self, message, opposite_ip, opposite_port):
        try:
            opposite_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            opposite_socket.connect((opposite_ip, opposite_port))
            opposite_socket.sendall(message.encode('utf-8'))
            opposite_socket.close()
        except Exception as e:
            print(f"Error occurred while sending message to opposite client: {e}")

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            print(f"Client disconnected: {client_socket.getpeername()}")
            self.clients.remove(client_socket)
            client_socket.close()

if __name__ == '__main__':
    server = ChatServer('0.0.0.0', 12345)
    server.start()
