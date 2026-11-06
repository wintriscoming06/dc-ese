# ==============================================================================
# EXPERIMENT 9: RING LEADER ELECTION ALGORITHM
# Description: Demonstrates election in a logical ring topology where an election
#              token traverses active nodes, selecting the highest-priority active node.
# CSV required: ring_nodes_31.csv (or data.csv)
# ==============================================================================

# Import csv module to parse ring network configuration
import csv

# Dictionary mapping node_id (int) -> active status (bool)
nodes = {}
# Dictionary mapping node_id (int) -> next neighbor node_id (int) in the logical ring
next_node = {}
# Dictionary mapping node_id (int) -> priority rank (int)
priority = {}

# Open the ring topology CSV file in read mode
with open("ring_nodes_31.csv", "r", newline="") as file:
    # Initialize the CSV reader object
    reader = csv.reader(file)
    # Skip the header row (node_id, next_id, active, priority_rank)
    next(reader)

    # Parse each node's configuration row
    for row in reader:
        node_id = int(row[0])                            # Column 0: Current node ID
        next_id = int(row[1])                            # Column 1: Next neighbor node ID in the ring
        active = row[2].strip().upper() == "TRUE"         # Column 2: Boolean active/alive flag
        priority_rank = int(row[3])                      # Column 3: Node's election priority ranking

        # Store properties in corresponding dictionaries
        nodes[node_id] = active
        next_node[node_id] = next_id
        priority[node_id] = priority_rank

# Designate Node 1 as the initiator that detects failure and initiates the ring election
initiator = 1
# Initialize token list with the initiator node ID as the first participant
token = [initiator]
# Point to the first recipient in the ring: the next neighbor of the initiator
current = next_node[initiator]

# Announce start of election by initiator
print("Election initiated by Node", initiator)

# Traverse the ring: pass election token around until it returns to the initiator
while current != initiator:
    # Check if the candidate node is currently active
    if nodes[current]:
        # Active node adds its ID to the token list
        token.append(current)
        # Log successful receipt of token by active node
        print("Token received by Node", current)
    else:
        # Inactive or crashed node is bypassed in the ring
        print("Node", current, "is inactive. Skipping.")

    # Move token to the next node in the ring sequence
    current = next_node[current]

# Select coordinator: iterate over all nodes that participated in the token
new_coordinator = token[0]  # Start by assuming the first participant is winner
for node in token:
    # If this participant has a strictly higher priority ranking than current candidate
    if priority[node] > priority[new_coordinator]:
        # Update winning coordinator to this higher-priority node
        new_coordinator = node

# Display list of all participating nodes that received the token
print("Participating nodes:", token)
# Display the newly elected coordinator node ID
print("New Coordinator:", new_coordinator)
# Display the winning priority score of the elected coordinator
print("Highest Priority:", priority[new_coordinator])
