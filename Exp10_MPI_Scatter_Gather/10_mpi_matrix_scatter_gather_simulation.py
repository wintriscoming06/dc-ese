# ==============================================================================
# EXPERIMENT 10: MATRIX MULTIPLICATION - MPI SCATTER/GATHER SIMULATION
# Description: Demonstrates MPI Scatter-Gather paradigm using concurrent threads
#              to distribute rows of a matrix (scatter), compute products in parallel,
#              and collect results back at the master (gather).
# CSV required: matrix_22.csv
# ==============================================================================

# Import csv module to parse matrix elements from CSV
import csv
# Import ThreadPoolExecutor to simulate parallel MPI worker processes
from concurrent.futures import ThreadPoolExecutor

# Master matrix list to hold rows read from CSV
matrix = []

# Open the matrix CSV file in read mode
with open("matrix_22.csv", "r", newline="") as file:
    # Create the CSV reader object
    reader = csv.reader(file)
    # Skip the header row (row_label, col1, col2, ...)
    next(reader)

    # Read each row of numbers from CSV
    for row in reader:
        # Slice from index 1 to ignore row label, convert string values to integers
        matrix.append([int(value) for value in row[1:]])

# Worker task function: calculates dot product of a given row against each matrix column (A x A)
def multiply_row(row):
    result_row = []  # List to store computed product values for this row

    # zip(*matrix) transposes the matrix, providing one column at a time
    for column in zip(*matrix):
        value = 0    # Accumulator for dot product of row and column

        # Multiply corresponding row and column elements and sum them up
        for i in range(len(row)):
            value += row[i] * column[i]

        # Append computed cell value to the output row
        result_row.append(value)

    # Return the fully computed row
    return result_row

# SCATTER PHASE: Master partitions and distributes rows among worker threads
print("MASTER: Scattering matrix rows to workers...")
# Enumerate through matrix rows to display assignment to workers
for worker_id, row in enumerate(matrix):
    # Log worker ID and the row data assigned to it
    print("Worker", worker_id, "received row", row)

# Execute parallel computation across worker pool simulating MPI distributed processes
with ThreadPoolExecutor() as executor:
    # Map the multiply_row task across all matrix rows concurrently
    result = list(executor.map(multiply_row, matrix))

# GATHER PHASE: Master collects and aggregates computed rows returned by workers
print("\nMASTER: Gathering results...")
# Display each gathered row received from the workers
for row in result:
    print(row)

# Display final aggregated matrix product (A x A)
print("\nFinal Matrix Product (A x A):")
# Iterate and print each row of the final multiplied matrix
for row in result:
    print(row)
