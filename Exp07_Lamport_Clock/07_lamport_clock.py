# ==============================================================================
# EXPERIMENT 7: LAMPORT'S LOGICAL CLOCK ALGORITHM
# Description: Demonstrates Lamport's algorithm for ordering events in a distributed
#              system, resolving causality and establishing a total order of events.
# CSV required: events_29.csv
# ==============================================================================

# Import csv module to parse events log
import csv

# Dictionary storing current scalar logical clock for each process
clock = {}
# Dictionary storing timestamp of sent messages, keyed by (sender, receiver)
messages = {}
# List to collect all event records for total ordering: (timestamp, process, event_id)
events = []

# Open the events CSV file in read mode
with open("events_29.csv", "r", newline="") as file:
    # Initialize CSV reader object
    reader = csv.reader(file)
    # Skip the header row (event_id, process, event_type, receiver, initial_clock)
    next(reader)

    # Process each recorded event row by row
    for row in reader:
        event_id = row[0]           # Column 0: Event identifier (e.g. E1, E2)
        process = row[1]            # Column 1: Process where event occurred (e.g. P1, P2)
        event_type = row[2]         # Column 2: Event type (SEND, RECEIVE, or INTERNAL)
        other_process = row[3]      # Column 3: Communication partner process
        initial = int(row[4])       # Column 4: Initial clock value if process has not started yet

        # If this process has not been registered yet, initialize its clock to initial value
        if process not in clock:
            clock[process] = initial

        # On a RECEIVE event, update local clock using Lamport's rule: max(local_clock, message_clock)
        if event_type == "RECEIVE":
            key = (other_process, process)          # Key format: (sender, receiver)
            received_time = messages.pop(key)       # Retrieve and remove timestamp sent with the message
            # Advance local clock to highest value between sender and receiver
            clock[process] = max(clock[process], received_time)

        # Lamport's rule: increment local clock by 1 for any event execution
        clock[process] += 1
        # Capture current updated timestamp
        timestamp = clock[process]
        # Display the event and its new timestamp
        print(event_id, process, event_type, "->", timestamp)

        # On a SEND event, store timestamp so the receiver can read it
        if event_type == "SEND":
            messages[(process, other_process)] = timestamp

        # Append tuple to events list for total ordering comparison
        events.append((timestamp, process, event_id))

# Print header for Total Ordering output
print("\nTOTAL ORDER")
# Sort events by timestamp; ties are deterministically broken by process name and event_id
events.sort()
# Display each event in its final total order sequence
for timestamp, process, event_id in events:
    # Print timestamp, process identifier, and event identifier
    print(timestamp, process, event_id)
