# ==============================================================================
# EXPERIMENT 3: BERKELEY CLOCK SYNCHRONIZATION ALGORITHM
# Description: Demonstrates internal clock synchronization where a master polls
#              slave clocks, filters faulty readings, computes the average,
#              and broadcasts adjustments to synchronize all nodes.
# CSV required: node_clocks_35.csv
# ==============================================================================

# Import csv module to parse node clock values and fault flags
import csv

# Dictionary mapping node name (str) -> clock time (int) for non-faulty nodes
nodes = {}

# Open the node clocks CSV file in read mode
with open("node_clocks_35.csv", "r", newline="") as file:
    # Create the CSV reader object
    reader = csv.reader(file)
    # Skip the header row (node, clock, is_faulty)
    next(reader)

    # Loop through each row in the CSV file
    for row in reader:
        node = row[0]                                   # Column 0: Node identifier (e.g. S1, S2, Master)
        clock_time = int(row[1])                        # Column 1: Clock reading in time units (converted to int)
        is_faulty = row[2].strip().upper() == "TRUE"    # Column 2: Boolean flag indicating if node clock is faulty

        # In Berkeley algorithm, readings from faulty or outlier nodes are discarded
        if is_faulty:
            # Log that this faulty node's clock reading is being ignored
            print("Discarding faulty node:", node)
        else:
            # Store the valid clock time in our dictionary with the node name as key
            nodes[node] = clock_time

# Print header for original clock readings
print("Original Clock Times:")
# Iterate through all valid nodes and display their original unadjusted clock times
for node, clock_time in nodes.items():
    # Print node name and its corresponding clock time
    print(node, ":", clock_time)

# Initialize total clock time accumulator to zero
total = 0
# Sum up all valid clock readings
for clock_time in nodes.values():
    # Add each node's clock time to the running total
    total += clock_time

# Compute average clock time across all non-faulty participating nodes
average = total / len(nodes)
# Display the computed system-wide average time
print("\nAverage Time:", average)

# Print header for calculated clock adjustments
print("\nClock Adjustments:")
# Iterate over each participating node to calculate the specific offset needed
for node, clock_time in nodes.items():
    # Calculate adjustment offset: difference between target average and current clock
    adjustment = average - clock_time
    # Calculate the new synchronized time after applying the adjustment
    new_time = clock_time + adjustment
    # Print the node, the required adjustment offset, and the resulting synchronized time
    print(node, "Adjustment:", adjustment, "New Time:", new_time)
