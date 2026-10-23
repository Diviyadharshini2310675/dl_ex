class Process:
    
    def __init__(self, name):
        self.name = name
        self.clock = 0

    def local_event(self):
        self.clock += 1

    def send(self):
        self.clock += 1
        return self.clock

    def receive(self, received_clock):
        self.clock = max(
            self.clock,
            received_clock
        ) + 1


p1 = Process("Process 1")
p2 = Process("Process 2")

n = int(input("Enter number of events: "))

for i in range(n):

    print("\nEvent", i + 1)

    print("1. Process 1 Local Event")
    print("2. Process 1 Send")
    print("3. Process 2 Local Event")
    print("4. Process 2 Send")
    print("5. Process 1 Receive")
    print("6. Process 2 Receive")

    choice = int(input("Enter choice: "))

    if choice == 1:

        p1.local_event()

        print(
            "Process 1 Clock:",
            p1.clock
        )

    elif choice == 2:

        message = p1.send()

        print(
            "Process 1 sent message",
            message
        )

    elif choice == 3:

        p2.local_event()

        print(
            "Process 2 Clock:",
            p2.clock
        )

    elif choice == 4:

        message = p2.send()

        print(
            "Process 2 sent message",
            message
        )

    elif choice == 5:

        received = int(
            input(
                "Enter timestamp received: "
            )
        )

        p1.receive(received)

        print(
            "Process 1 Clock:",
            p1.clock
        )

    elif choice == 6:

        received = int(
            input(
                "Enter timestamp received: "
            )
        )

        p2.receive(received)

        print(
            "Process 2 Clock:",
            p2.clock
        )

    else:

        print("Invalid choice")

print("\n----- FINAL CLOCKS -----")

print("Process 1:", p1.clock)
print("Process 2:", p2.clock)