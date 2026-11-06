# ==============================================================================
# EXPERIMENT 4: MULTITHREADING AND MUTEX SYNCHRONIZATION
# Description: Demonstrates concurrent worker threads processing tasks and using
#              a mutual exclusion (Mutex) lock to safely update shared state.
# CSV required: tasks_50.csv
# ==============================================================================

# Import csv module for reading task data
import csv
# Import threading module for creating and synchronizing threads
import threading
# Import time module to simulate task execution duration
import time

# List to hold all raw task records loaded from the CSV
tasks = []

# Open the task CSV file in read mode
with open("tasks_50.csv", "r", newline="") as file:
    # Initialize CSV reader object
    reader = csv.reader(file)
    # Skip the CSV header row (task_id, worker, duration_ms, priority, status)
    next(reader)
    # Iterate through each row in the CSV
    for row in reader:
        # Append the row list representing a task to the tasks list
        tasks.append(row)

# Shared resource list where finished task IDs are recorded by threads
completed_tasks = []
# Create a Mutex Lock object to protect shared resources and prevent race conditions
lock = threading.Lock()

# Worker function executed concurrently by each thread
def worker(name, assigned_tasks):
    # Iterate over all tasks specifically assigned to this worker thread
    for task in assigned_tasks:
        # Log that this worker has started processing the task
        print(name, "processing", task[0])

        # Simulate execution time by sleeping (CSV duration is in milliseconds, so divide by 1000)
        time.sleep(int(task[2]) / 1000)

        # Log that the worker is requesting access to the critical section
        print(name, "waiting for lock")

        # Acquire lock entering critical section (automatically released on exit)
        with lock:
            # Log that lock has been successfully acquired
            print(name, "acquired lock")
            # Safely append the completed task ID to the shared list
            completed_tasks.append(task[0])
            # Update the task status to COMPLETED in the task record
            task[4] = "COMPLETED"
            # Log that lock is about to be released
            print(name, "released lock")

# Dictionary to partition and group tasks by their assigned worker name
tasks_by_worker = {}
# Iterate through each task to group them
for task in tasks:
    worker_name = task[1]  # Column 1 contains worker identifier (e.g. Worker-1)
    # If this worker does not have an entry in dictionary yet, initialize an empty list
    if worker_name not in tasks_by_worker:
        tasks_by_worker[worker_name] = []
    # Add the current task to the worker's assigned list
    tasks_by_worker[worker_name].append(task)

# List to keep track of all created Thread objects
threads = []

# Instantiate and launch one thread per unique worker
for worker_name, assigned_tasks in tasks_by_worker.items():
    # Create thread with worker function as target and worker details as arguments
    thread = threading.Thread(
        target=worker,
        args=(worker_name, assigned_tasks)
    )
    # Keep reference to thread in our list
    threads.append(thread)
    # Start thread execution asynchronously
    thread.start()

# Wait for all worker threads to finish before proceeding to the final summary
for thread in threads:
    # Block calling thread until this worker thread terminates
    thread.join()

# Print final list of completed tasks across all threads
print("\nCompleted tasks:", completed_tasks)
# Print status of each individual task confirming completion
for task in tasks:
    # Print task ID and its updated status string
    print(task[0], task[4])
