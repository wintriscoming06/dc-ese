# EXPERIMENT 7: LAMPORT'S LOGICAL CLOCK
# CSV required: events_29.csv
import csv

clock = {}      # Current logical clock for each process.
messages = {}   # Timestamp of each sent message.
events = []     # Event records for final timestamp ordering.

with open("events_29.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.

    for row in reader:
        event_id = row[0]
        process = row[1]
        event_type = row[2]
        other_process = row[3]
        initial = int(row[4])

        # Initialise a process clock when first encountered.
        if process not in clock:
            clock[process] = initial

        # A receive event merges the local clock with message timestamp.
        if event_type == "RECEIVE":
            key = (other_process, process)  # (sender, receiver).
            received_time = messages.pop(key)
            clock[process] = max(clock[process], received_time)

        # Increment clock for local, send, and receive events.
        clock[process] += 1
        timestamp = clock[process]
        print(event_id, process, event_type, "->", timestamp)

        # Save timestamp when a message is sent.
        if event_type == "SEND":
            messages[(process, other_process)] = timestamp

        events.append((timestamp, process, event_id))

print("\nTOTAL ORDER")
events.sort()  # Sort by timestamp; process and event IDs break ties.
for timestamp, process, event_id in events:
    print(timestamp, process, event_id)
