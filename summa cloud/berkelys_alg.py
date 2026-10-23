n = int(input("Enter number of systems: "))

clocks = []

for i in range(n):

    clock = float(
        input(f"Enter clock time of System {i + 1}: ")
    )

    clocks.append(clock)

print("\nOriginal Clock Times:")
print(clocks)

# First system is master
master = clocks[0]

differences = []

for clock in clocks:
    differences.append(clock - master)

print("\nClock Differences:")
print(differences)

average_difference = sum(differences) / n

print(
    "\nAverage Difference:",
    average_difference
)

print("\n----- ADJUSTED CLOCKS -----")

for i in range(n):

    adjusted_clock = master + average_difference

    print(
        f"System {i + 1}:",
        round(adjusted_clock, 2)
    )