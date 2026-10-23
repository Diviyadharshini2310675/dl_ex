n = int(input("Enter number of tasks: "))

tasks = []

for i in range(n):

    time = int(
        input(
            f"Enter processing time for Task {i + 1}: "
        )
    )

    tasks.append(time)


worker1_time = 0
worker2_time = 0

worker1_count = 0
worker2_count = 0

print("\n----- TASK SCHEDULING -----")

for i in range(n):

    task_name = f"Task {i + 1}"

    processing_time = tasks[i]

    # Round Robin
    if i % 2 == 0:

        worker = "Worker 1"

        start_time = worker1_time

        completion_time = (
            start_time + processing_time
        )

        worker1_time = completion_time

        worker1_count += 1

    else:

        worker = "Worker 2"

        start_time = worker2_time

        completion_time = (
            start_time + processing_time
        )

        worker2_time = completion_time

        worker2_count += 1

    print(
        task_name,
        "->",
        worker,
        "| Processing Time:",
        processing_time,
        "| Completion Time:",
        completion_time
    )


print("\n----- SUMMARY -----")

print(
    "Number of tasks assigned to Worker 1:",
    worker1_count
)

print(
    "Number of tasks assigned to Worker 2:",
    worker2_count
)

print(
    "Worker 1 total completion time:",
    worker1_time
)

print(
    "Worker 2 total completion time:",
    worker2_time
)