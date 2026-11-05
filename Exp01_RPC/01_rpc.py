# EXPERIMENT 1: RMI / RPC SIMULATION
# CSV required: rpc_calls_33.csv
import csv

# Server procedure 1: receives an amount and returns a processed value.
def processData(amount):
    print("[SERVER] Processing:", amount)
    return amount + 50

# Server procedure 2: checks whether the donation meets the minimum.
def checkDonation(amount):
    print("[SERVER] Checking donation:", amount)
    if amount >= 500:
        return "Eligible donation"
    return "Below minimum donation"

# Map the procedure name sent by the client to its actual Python function.
methods = {
    "processData": processData,
    "checkDonation": checkDonation
}

# Read the client requests from the CSV file.
with open("rpc_calls_33.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row.

    for row in reader:
        call_id = row[0]             # Request ID.
        client = row[1]              # Client name.
        method_name = row[2]         # Requested server procedure.
        parameter = int(row[3])      # Convert CSV text to integer.

        print("\n[DISPATCH]", call_id, client, "invoking", method_name)

        # Check that the requested procedure exists.
        if method_name in methods:
            result = methods[method_name](parameter)  # Execute procedure.
            print("[RETURN] Result:", result)
        else:
            print("[RETURN] Unknown method")
