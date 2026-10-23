import socket

client = socket.socket()
client.connect(("localhost", 9999))

message = input("Enter message to server: ")

client.send(message.encode())

reply = client.recv(1024).decode()

print("Reply from Server:", reply)

client.close()