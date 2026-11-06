# ==============================================================================
# EXPERIMENT 6: VECTOR CLOCKS AND CAUSAL RELATIONSHIPS
# Description: Demonstrates vector clock maintenance across distributed processes
#              (P1, P2, P3) and analyzes pairwise causal relationships
#              (causally preceding vs concurrent).
# CSV required: vector_events_36.csv
# ==============================================================================

# Import csv module to parse distributed events from CSV
import csv

# Ordered list of processes in the distributed system
processes = ["P1", "P2", "P3"]
# Dictionary to store the current vector clock for each process
clocks = {}

# Initialize each process with a 3-element zero vector [0, 0, 0]
for process in processes:
    clocks[process] = [0, 0, 0]

# Dictionary to hold message transit vectors, keyed by (sender, receiver) tuple
messages = {}
# List to record each processed event along with its resulting vector clock snapshot
events = []

# Open the vector events CSV file in read mode
with open("vector_events_36.csv", "r", newline="") as file:
    # Initialize the CSV reader
    reader = csv.reader(file)
    # Skip the header row (event_id, process, action, target)
    next(reader)

    # Process events sequentially row by row
    for row in reader:
        event_id = row[0]                   # Column 0: Event identifier (e.g. e1, e2)
        process = row[1]                    # Column 1: Process executing the event (P1, P2, P3)
        action = row[2]                     # Column 2: Type of action (SEND, RECEIVE, LOCAL)
        target = row[3]                     # Column 3: Destination or source process
        index = processes.index(process)    # Find position index (0, 1, or 2) of this process in vector

        # On RECEIVE event, update local clock by taking pairwise maximum with sender's vector
        if action == "RECEIVE":
            key = (target, process)         # Key representing message channel (sender, receiver)
            received_vector = messages.pop(key)  # Retrieve and remove sender's vector from transit

            # Update each element of local vector with maximum of local and received value
            for i in range(3):
                clocks[process][i] = max(
                    clocks[process][i], received_vector[i]
                )

        # Always increment the process's own vector component for every event (SEND, RECEIVE, LOCAL)
        clocks[process][index] += 1
        # Create an independent copy of current vector clock snapshot
        current_vector = clocks[process].copy()
        # Print event execution log and resulting vector timestamp
        print(event_id, process, action, "->", current_vector)

        # If action is SEND, save the current vector so it can be delivered with the message
        if action == "SEND":
            messages[(process, target)] = current_vector.copy()

        # Record this event ID and its vector timestamp for pairwise causality analysis
        events.append((event_id, current_vector))

# Function to determine if vector 'a' causally happens before vector 'b' (a -> b)
def happens_before(a, b):
    all_less_or_equal = True    # Must satisfy: a[i] <= b[i] for all i
    one_strictly_less = False   # Must satisfy: a[i] < b[i] for at least one i

    # Compare corresponding vector clock components element-wise
    for i in range(3):
        # If any component of a exceeds b, then a cannot happen before b
        if a[i] > b[i]:
            all_less_or_equal = False
        # If any component of a is strictly smaller than b, flag condition as met
        if a[i] < b[i]:
            one_strictly_less = True

    # 'a' happens before 'b' if and only if both conditions hold true
    return all_less_or_equal and one_strictly_less

# Print header for pairwise causality analysis
print("\nPAIRWISE EVENT RELATIONSHIPS")
# Compare every pair of recorded events (i, j) where i < j
for i in range(len(events)):
    for j in range(i + 1, len(events)):
        id_a, vector_a = events[i]  # Event A details
        id_b, vector_b = events[j]  # Event B details

        # Check if Event A causally precedes Event B
        if happens_before(vector_a, vector_b):
            print(id_a, "<", id_b, "(causally preceding)")
        # Check if Event B causally precedes Event A
        elif happens_before(vector_b, vector_a):
            print(id_b, "<", id_a, "(causally preceding)")
        # If neither happens before the other, the events are concurrent
        else:
            print(id_a, "||", id_b, "(concurrent)")
