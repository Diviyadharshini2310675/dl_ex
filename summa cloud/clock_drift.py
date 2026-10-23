duration = int(
    input("Enter simulation time in seconds: ")
)

drift = float(
    input(
        "Enter Clock B drift per second "
        "(in milliseconds): "
    )
)

clock_a = 0
clock_b = 0

print("\nTime\tClock A\tClock B\tDifference")

for second in range(1, duration + 1):

    clock_a += 1000

    clock_b += 1000 + drift

    difference = clock_b - clock_a

    print(
        second,
        "\t",
        clock_a,
        "\t",
        clock_b,
        "\t",
        difference
    )

print("\n----- FINAL RESULT -----")

print(
    "Clock A:",
    clock_a,
    "milliseconds"
)

print(
    "Clock B:",
    clock_b,
    "milliseconds"
)

print(
    "Difference:",
    clock_b - clock_a,
    "milliseconds"
)

print(
    "Difference:",
    (clock_b - clock_a) / 1000,
    "seconds"
)