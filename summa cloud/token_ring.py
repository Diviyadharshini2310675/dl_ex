import time

n = int(input("Enter number of processes: "))

rounds = int(input("Enter number of token rounds: "))

processes = []

for i in range(n):
    processes.append(i + 1)

print("\nProcesses in Ring:")
print(processes)

token = 0

print("\n----- TOKEN RING -----")

for i in range(rounds):

    process = processes[token]

    print("\nToken received by Process", process)

    print("Process", process, "enters Critical Section")

    time.sleep(1)

    print("Process", process, "exits Critical Section")

    token = (token + 1) % n

    print(
        "Token passed to Process",
        processes[token]
    )