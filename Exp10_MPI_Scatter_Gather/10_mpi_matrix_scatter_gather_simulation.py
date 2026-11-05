# EXPERIMENT 10: MATRIX MULTIPLICATION - SCATTER/GATHER SIMULATION
# CSV required: matrix_22.csv
# This is a local thread-based simulation, not actual MPI/mpi4py execution.
import csv
from concurrent.futures import ThreadPoolExecutor

matrix = []

# Read matrix values from CSV. The first column contains row labels.
with open("matrix_22.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip column headings.

    for row in reader:
        matrix.append([int(value) for value in row[1:]])

# Each worker calculates one output row of A x A.
def multiply_row(row):
    result_row = []

    # zip(*matrix) produces one column at a time.
    for column in zip(*matrix):
        value = 0

        # Calculate the dot product of this row and this column.
        for i in range(len(row)):
            value += row[i] * column[i]

        result_row.append(value)

    return result_row

# SCATTER: master distributes matrix rows to workers.
print("MASTER: Scattering matrix rows to workers...")
for worker_id, row in enumerate(matrix):
    print("Worker", worker_id, "received row", row)

# Parallel row calculations using a local thread pool.
with ThreadPoolExecutor() as executor:
    result = list(executor.map(multiply_row, matrix))

# GATHER: master collects the rows returned by workers.
print("\nMASTER: Gathering results...")
for row in result:
    print(row)

print("\nFinal Matrix Product (A x A):")
for row in result:
    print(row)
