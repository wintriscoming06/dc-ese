# EXPERIMENT 3: BERKELEY CLOCK SYNCHRONIZATION
# CSV required: node_clocks_35.csv
import csv

nodes = {}  # Stores only valid node clock readings.

# Read clock values and fault status.
with open("node_clocks_35.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header.

    for row in reader:
        node = row[0]
        clock_time = int(row[1])
        is_faulty = row[2].strip().upper() == "TRUE"

        # Ignore faulty nodes as required by the question slip.
        if is_faulty:
            print("Discarding faulty node:", node)
        else:
            nodes[node] = clock_time

print("\nOriginal Clock Times:")
for node, clock_time in nodes.items():
    print(node, ":", clock_time)

# Calculate the average of valid clocks.
if nodes:
    total = 0
    for clock_time in nodes.values():
        total += clock_time

    average = total / len(nodes)
    print("\nAverage Time:", average)

    # Calculate how much each valid node must adjust its clock.
    print("\nClock Adjustments:")
    for node, clock_time in nodes.items():
        adjustment = average - clock_time
        new_time = clock_time + adjustment
        print(node, "Adjustment:", adjustment, "New Time:", new_time)
else:
    print("No valid clocks available.")
