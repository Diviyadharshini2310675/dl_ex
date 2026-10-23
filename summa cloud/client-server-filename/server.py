import socket
import os

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Server waiting...")

conn, addr = server.accept()

filename = conn.recv(1024).decode()

if os.path.exists(filename):

    with open(filename, "r") as file:
        content = file.read()

    lines = len(content.splitlines())
    words = len(content.split())
    size = os.path.getsize(filename)

    response = f"""
File Name: {filename}
Number of Lines: {lines}
Number of Words: {words}
File Size: {size} bytes
"""

else:
    response = "File not found."

conn.send(response.encode())

conn.close()
server.close()