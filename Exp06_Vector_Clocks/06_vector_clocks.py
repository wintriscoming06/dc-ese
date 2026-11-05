# EXPERIMENT 6: VECTOR CLOCKS
# CSV required: vector_events_36.csv
# Process order determines vector positions: P1, P2, P3.
import csv

processes = ["P1", "P2", "P3"]
clocks = {}

# Each process starts with a zero vector.
for process in processes:
    clocks[process] = [0, 0, 0]

messages = {}  # Stores vectors attached to messages.
events = []    # Stores each event and its vector timestamp.

with open("vector_events_36.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header.

    for row in reader:
        event_id = row[0]
        process = row[1]
        action = row[2]
        target = row[3]
        index = processes.index(process)

        # On RECEIVE, merge local vector with the received vector.
        if action == "RECEIVE":
            key = (target, process)  # (sender, receiver).
            received_vector = messages.pop(key)

            for i in range(3):
                clocks[process][i] = max(
                    clocks[process][i], received_vector[i]
                )

        # Increment this process's own component for every event.
        clocks[process][index] += 1
        current_vector = clocks[process].copy()
        print(event_id, process, action, "->", current_vector)

        # On SEND, attach a copy of the current vector to the message.
        if action == "SEND":
            messages[(process, target)] = current_vector.copy()

        events.append((event_id, current_vector))

# Return True when vector a causally happens before vector b.
def happens_before(a, b):
    all_less_or_equal = True
    one_strictly_less = False

    for i in range(3):
        if a[i] > b[i]:
            all_less_or_equal = False
        if a[i] < b[i]:
            one_strictly_less = True

    return all_less_or_equal and one_strictly_less

print("\nPAIRWISE EVENT RELATIONSHIPS")
for i in range(len(events)):
    for j in range(i + 1, len(events)):
        id_a, vector_a = events[i]
        id_b, vector_b = events[j]

        if happens_before(vector_a, vector_b):
            print(id_a, "<", id_b, "(causally preceding)")
        elif happens_before(vector_b, vector_a):
            print(id_b, "<", id_a, "(causally preceding)")
        else:
            print(id_a, "||", id_b, "(concurrent)")
