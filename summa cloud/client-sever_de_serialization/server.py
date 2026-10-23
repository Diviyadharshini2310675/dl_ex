import socket
import pickle

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Server waiting...")

conn, addr = server.accept()

data = conn.recv(4096)

# Deserialization
student = pickle.loads(data)

print("\nReceived Student Details:")
print(student)

student["status"] = "Processed by Server"

# Serialization
response = pickle.dumps(student)

conn.send(response)

conn.close()
server.close()