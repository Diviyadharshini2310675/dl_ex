import socket

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Server is waiting for client...")

conn, addr = server.accept()
print("Connected to:", addr)

message = conn.recv(1024).decode()

print("Message from Client:", message)

reply = input("Enter reply to client: ")

conn.send(reply.encode())

conn.close()
server.close()