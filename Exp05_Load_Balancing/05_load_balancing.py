# ==============================================================================
# EXPERIMENT 5: DYNAMIC LOAD BALANCING ALGORITHMS
# Description: Demonstrates Round Robin and Least Connections load balancing
#              strategies to distribute workloads among available backend workers.
# CSV required: workload_43.csv
# ==============================================================================

# Import csv module to parse incoming job workload data
import csv

# List to hold tuples of (job_id, compute_units)
jobs = []

# Open the workload CSV file in read mode
with open("workload_43.csv", "r", newline="") as file:
    # Create the CSV reader object
    reader = csv.reader(file)
    # Skip the header row (job_id, compute_units)
    next(reader)
    # Loop through each row to extract jobs
    for row in reader:
        # Append tuple with job ID string and compute units converted to integer
        jobs.append((row[0], int(row[1])))

# Define list of available server workers
workers = ["W1", "W2", "W3"]

# ---------------- ROUND ROBIN LOAD BALANCING ----------------
print("\nROUND ROBIN")
# Dictionary tracking total compute load accumulated on each worker
load = {"W1": 0, "W2": 0, "W3": 0}
# Dictionary tracking total count of jobs assigned to each worker
count = {"W1": 0, "W2": 0, "W3": 0}

# Iterate through every incoming job by index
for i in range(len(jobs)):
    # Retrieve current job tuple
    job = jobs[i]
    # Modulo operator selects worker cyclically based on job index
    worker_index = i % len(workers)
    # Get the selected worker ID
    worker = workers[worker_index]

    # Add the job's compute units to the selected worker's total load
    load[worker] += job[1]
    # Increment the selected worker's assigned job count by 1
    count[worker] += 1
    # Print job assignment log
    print(job[0], "->", worker)

# Print cumulative compute load assigned to each worker under Round Robin
print("Compute Load:", load)
# Print total number of jobs assigned to each worker under Round Robin
print("Jobs per Worker:", count)

# ---------------- LEAST CONNECTIONS LOAD BALANCING ----------------
print("\nLEAST CONNECTIONS")
# Initialize baseline active connection counts for each worker before new jobs arrive
count = {"W1": 2, "W2": 1, "W3": 3}
# Reset cumulative load tracking for Least Connections simulation
load = {"W1": 0, "W2": 0, "W3": 0}

# Iterate through each job in the incoming queue
for job in jobs:
    # Assume first worker has least connections as initial candidate
    selected_worker = workers[0]

    # Scan through all available workers to find the one with minimum active connections
    for worker in workers:
        # If current worker has fewer connections than current minimum candidate
        if count[worker] < count[selected_worker]:
            # Update candidate to this worker with fewer connections
            selected_worker = worker

    # Add compute load of the job to the chosen worker
    load[selected_worker] += job[1]
    # Increment active connection count for the chosen worker
    count[selected_worker] += 1
    # Print the assignment decision log
    print(job[0], "->", selected_worker)

# Print cumulative compute load assigned under Least Connections
print("Compute Load:", load)
# Print final active connection count for each worker
print("Final Connections:", count)
