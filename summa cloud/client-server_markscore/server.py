import socket

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Server waiting...")

conn, addr = server.accept()

data = conn.recv(4096).decode()

marks = list(map(int, data.split(",")))

total = sum(marks)
average = total / len(marks)

# Pass / Fail
if all(mark >= 40 for mark in marks):
    result = "PASS"
else:
    result = "FAIL"

# Grade
if average >= 90:
    grade = "A"
elif average >= 80:
    grade = "B"
elif average >= 70:
    grade = "C"
elif average >= 60:
    grade = "D"
else:
    grade = "F"

# Simple rank based on average
if average >= 90:
    rank = 1
elif average >= 80:
    rank = 2
elif average >= 70:
    rank = 3
elif average >= 60:
    rank = 4
else:
    rank = 5

response = f"""
Total Marks: {total}
Average: {average:.2f}
Grade: {grade}
Result: {result}
Rank: {rank}
"""

conn.send(response.encode())

conn.close()
server.close()
