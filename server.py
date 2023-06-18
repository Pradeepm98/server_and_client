import socket

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = ''  # Empty string represents all available interfaces
server_port = 12345
server_socket.bind((server_host, server_port))
server_socket.listen(1)  # Listen for incoming connections
print(f"Server listening on {server_host}:{server_port}")

# Accept client connections
client_socket, client_address = server_socket.accept()
client_ip = client_address[0]
client_port = client_address[1]
print(f"Connected to client: {client_ip}:{client_port}")

# Receive and send messages to the client
while True:
  # Receive data from the client
  data = client_socket.recv(1024).decode()
  if not data:
    break

  print(f"Client ({client_ip}:{client_port}): {data}")

  # Send a response back to the client
  response = "Message received by the server."
  client_socket.send(response.encode())

# Close the connection
client_socket.close()
server_socket.close()
