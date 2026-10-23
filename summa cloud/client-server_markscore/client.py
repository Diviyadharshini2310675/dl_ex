import socket

client = socket.socket()
client.connect(("localhost", 9999))

n = int(input("Enter number of subjects: "))

marks = []

for i in range(n):
    mark = int(input(f"Enter marks for subject {i + 1}: "))
    marks.append(mark)

data = ",".join(map(str, marks))

client.send(data.encode())

response = client.recv(4096).decode()

print("\n----- RESULT -----")
print(response)

client.close()