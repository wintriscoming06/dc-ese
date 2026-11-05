# EXPERIMENT 5: LOAD BALANCING - ROUND ROBIN AND LEAST CONNECTIONS
# CSV required: workload_43.csv
import csv

jobs = []

# Read job IDs and compute requirements from CSV.
with open("workload_43.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.
    for row in reader:
        jobs.append((row[0], int(row[1])))

workers = ["W1", "W2", "W3"]

# ---------------- ROUND ROBIN ----------------
print("\nROUND ROBIN")
load = {"W1": 0, "W2": 0, "W3": 0}
count = {"W1": 0, "W2": 0, "W3": 0}

for i in range(len(jobs)):
    job = jobs[i]
    worker_index = i % len(workers)  # Cycles through worker indexes.
    worker = workers[worker_index]

    load[worker] += job[1]  # Add compute units assigned to this worker.
    count[worker] += 1      # Count the assigned job.
    print(job[0], "->", worker)

print("Compute Load:", load)
print("Jobs per Worker:", count)

# ---------------- LEAST CONNECTIONS ----------------
print("\nLEAST CONNECTIONS")
# Example initial active connection counts.
count = {"W1": 2, "W2": 1, "W3": 3}
load = {"W1": 0, "W2": 0, "W3": 0}

for job in jobs:
    selected_worker = workers[0]

    # Find the worker with the smallest connection count.
    for worker in workers:
        if count[worker] < count[selected_worker]:
            selected_worker = worker

    load[selected_worker] += job[1]
    count[selected_worker] += 1  # Assign one more connection/job.
    print(job[0], "->", selected_worker)

print("Compute Load:", load)
print("Final Connections:", count)
