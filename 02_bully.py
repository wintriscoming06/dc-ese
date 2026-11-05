# EXPERIMENT 2: BULLY LEADER ELECTION
# CSV required: bully_cluster_340.csv
import csv

nodes = {}                # node ID -> True if alive.
coordinator_status = {}   # node ID -> True if current coordinator.

# Read node status from the CSV file.
with open("bully_cluster_340.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.

    for row in reader:
        node_id = int(row[0])
        nodes[node_id] = row[1].strip().upper() == "TRUE"
        coordinator_status[node_id] = row[2].strip().upper() == "TRUE"

# Find the node currently marked as coordinator.
coordinator = None
for node_id in nodes:
    if coordinator_status[node_id]:
        coordinator = node_id
        break

# If the coordinator is alive, no election is required.
if coordinator is not None and nodes[coordinator]:
    print("Coordinator", coordinator, "is active.")
else:
    print("Coordinator", coordinator, "has failed.")

    # Collect all nodes that are currently alive.
    alive_nodes = []
    for node_id in nodes:
        if nodes[node_id]:
            alive_nodes.append(node_id)

    if alive_nodes:
        # Start the demonstration from the lowest-ID alive node.
        initiator = min(alive_nodes)
        print("Node", initiator, "starts election.")

        # Send ELECTION messages to all higher-ID alive nodes.
        higher_nodes = []
        for node_id in alive_nodes:
            if node_id > initiator:
                higher_nodes.append(node_id)
                print("ELECTION:", initiator, "->", node_id)

        # Higher alive nodes respond with OK.
        for node_id in higher_nodes:
            print("OK:", node_id, "->", initiator)

        # The highest-ID alive node wins.
        new_coordinator = max(alive_nodes)
        print("Node", new_coordinator, "wins the election.")

        # Announce the new coordinator to every alive node.
        for node_id in alive_nodes:
            print("COORDINATOR:", new_coordinator, "->", node_id)

        print("New Coordinator:", new_coordinator)
    else:
        print("No alive nodes available.")
