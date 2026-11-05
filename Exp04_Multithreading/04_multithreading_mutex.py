# EXPERIMENT 4: MULTITHREADING USING MUTEX LOCKS
# CSV required: tasks_50.csv
import csv
import threading
import time

tasks = []

# Read tasks from CSV into a list.
with open("tasks_50.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.
    for row in reader:
        tasks.append(row)

completed_tasks = []          # Shared list accessed by multiple threads.
lock = threading.Lock()       # Mutex protects the shared list and task status.

# Each worker thread executes this function.
def worker(name, assigned_tasks):
    for task in assigned_tasks:
        print(name, "processing", task[0])

        # Simulate task duration; CSV value is in milliseconds.
        time.sleep(int(task[2]) / 1000)

        print(name, "waiting for lock")

        # Only one thread can enter this critical section at a time.
        with lock:
            print(name, "acquired lock")
            completed_tasks.append(task[0])
            task[4] = "COMPLETED"
            print(name, "released lock")
        # The lock is automatically released after the with block.

# Group rows by the worker name specified in the CSV.
tasks_by_worker = {}
for task in tasks:
    worker_name = task[1]
    if worker_name not in tasks_by_worker:
        tasks_by_worker[worker_name] = []
    tasks_by_worker[worker_name].append(task)

threads = []

# Create and start one thread for each worker.
for worker_name, assigned_tasks in tasks_by_worker.items():
    thread = threading.Thread(
        target=worker,
        args=(worker_name, assigned_tasks)
    )
    threads.append(thread)
    thread.start()

# Wait until every worker thread has finished.
for thread in threads:
    thread.join()

print("\nCompleted tasks:", completed_tasks)
for task in tasks:
    print(task[0], task[4])
