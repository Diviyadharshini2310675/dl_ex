import socket
import pickle

client = socket.socket()
client.connect(("localhost", 9999))

name = input("Enter student name: ")
roll = input("Enter roll number: ")
department = input("Enter department: ")
marks = int(input("Enter marks: "))

student = {
    "name": name,
    "roll_no": roll,
    "department": department,
    "marks": marks
}

# Serialization
data = pickle.dumps(student)

client.send(data)

response = client.recv(4096)

# Deserialization
result = pickle.loads(response)

print("\n----- SERVER RESPONSE -----")
print(result)

client.close()