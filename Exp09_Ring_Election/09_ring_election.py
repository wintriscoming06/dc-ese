# EXPERIMENT 9: RING LEADER ELECTION
# CSV required: ring_nodes_31.csv
# This version follows the uploaded code PDF: highest-priority active node wins.
import csv

nodes = {}       # Node ID -> active status.
next_node = {}   # Node ID -> next node in ring.
priority = {}    # Node ID -> priority value.

with open("ring_nodes_31.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.

    for row in reader:
        node_id = int(row[0])
        next_id = int(row[1])
        active = row[2].strip().upper() == "TRUE"
        priority_rank = int(row[3])

        nodes[node_id] = active
        next_node[node_id] = next_id
        priority[node_id] = priority_rank

initiator = 1
token = [initiator]  # Election token starts with initiator.
current = next_node[initiator]

print("Election initiated by Node", initiator)

# Pass token around the ring until it returns to initiator.
while current != initiator:
    if nodes[current]:
        token.append(current)
        print("Token received by Node", current)
    else:
        print("Node", current, "is inactive. Skipping.")

    current = next_node[current]

# Select highest-priority active participant.
new_coordinator = token[0]
for node in token:
    if priority[node] > priority[new_coordinator]:
        new_coordinator = node

print("Participating nodes:", token)
print("New Coordinator:", new_coordinator)
print("Highest Priority:", priority[new_coordinator])

# If your assigned slip says highest NODE ID instead of highest priority,
# replace the selection section above with: new_coordinator = max(token).
