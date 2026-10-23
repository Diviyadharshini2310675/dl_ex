import socket

client = socket.socket()
client.connect(("localhost", 9999))

filename = input("Enter filename: ")

client.send(filename.encode())

response = client.recv(4096).decode()

print("\n----- FILE DETAILS -----")
print(response)

client.close()