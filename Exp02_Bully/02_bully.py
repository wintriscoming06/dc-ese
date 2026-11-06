# ==============================================================================
# EXPERIMENT 2: BULLY LEADER ELECTION ALGORITHM
# Description: Demonstrates election in distributed systems where the node with the
#              highest active ID bullies lower IDs and claims coordinator role.
# CSV required: bully_cluster_340.csv (or bully_cluster_34.csv)
# ==============================================================================

# Import standard csv module to read cluster nodes and their alive/coordinator statuses
import csv

# Dictionary mapping node_id (int) -> is_alive (bool)
nodes = {}
# Dictionary mapping node_id (int) -> is_current_coordinator (bool)
coordinator_status = {}

# Open the cluster configuration CSV file in read mode
with open("bully_cluster_340.csv", "r", newline="") as file:
    # Create the CSV reader object
    reader = csv.reader(file)
    # Skip the header row (node_id, is_alive, is_current_coordinator)
    next(reader)

    # Iterate over each row to populate node information
    for row in reader:
        node_id = int(row[0])                                           # Column 0: Node identifier (converted to integer)
        nodes[node_id] = row[1].strip().upper() == "TRUE"               # Column 1: Convert string 'TRUE'/'FALSE' to boolean alive status
        coordinator_status[node_id] = row[2].strip().upper() == "TRUE"  # Column 2: Convert string 'TRUE'/'FALSE' to boolean coordinator flag

# Initialize variable to store the ID of the current coordinator
coordinator = None

# Search through the dictionary to find which node was marked as the active coordinator
for node_id in nodes:
    # If this node has the coordinator flag set to True
    if coordinator_status[node_id]:
        # Assign coordinator variable to this node ID
        coordinator = node_id
        # Break the loop since there can be only one coordinator initially
        break

# Check if a coordinator was found and whether that coordinator node is currently alive
if coordinator is not None and nodes[coordinator]:
    # If the coordinator is alive, system is healthy, so no election is triggered
    print("Coordinator", coordinator, "is active.")
else:
    # If the coordinator has failed or is None, election must be initiated
    print("Coordinator", coordinator, "has failed.")

    # Initialize a list to hold all node IDs that are currently alive
    alive_nodes = []
    # Iterate over all node IDs in the cluster
    for node_id in nodes:
        # Check if the current node is alive
        if nodes[node_id]:
            # Add alive node ID to our list of alive nodes
            alive_nodes.append(node_id)

    # Check if there is at least one active node available to run the election
    if alive_nodes:
        # The lowest-ID active node detects the failure and initiates the election
        initiator = min(alive_nodes)
        # Announce that this node is starting the election process
        print("Node", initiator, "starts election.")

        # Initialize a list to store higher ID nodes that should receive election messages
        higher_nodes = []
        # Check all alive nodes to find those with higher ID than the initiator
        for node_id in alive_nodes:
            # If the node has an ID strictly greater than the initiator
            if node_id > initiator:
                # Add it to the higher_nodes list
                higher_nodes.append(node_id)
                # Print the ELECTION message transmission from initiator to the higher node
                print("ELECTION:", initiator, "->", node_id)

        # All higher alive nodes reply with an OK message to take over the election
        for node_id in higher_nodes:
            # Print that the higher node sends an OK message back to the initiator
            print("OK:", node_id, "->", initiator)

        # In Bully algorithm, the alive node with the absolute maximum ID wins the election
        new_coordinator = max(alive_nodes)
        # Announce the winning node of the election
        print("Node", new_coordinator, "wins the election.")

        # The new coordinator broadcasts COORDINATOR announcement to all alive nodes
        for node_id in alive_nodes:
            # Print the announcement message sent to each alive node
            print("COORDINATOR:", new_coordinator, "->", node_id)

        # Print the final elected coordinator
        print("New Coordinator:", new_coordinator)
    else:
        # Handle edge case where no nodes in the cluster are alive
        print("No alive nodes available.")
