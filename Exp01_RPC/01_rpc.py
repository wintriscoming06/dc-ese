# ==============================================================================
# EXPERIMENT 1: REMOTE PROCEDURE CALL (RPC) / RMI SIMULATION
# Description: Demonstrates client-to-server procedure dispatch using a dictionary
#              dispatch table, reading requests from a CSV file.
# CSV required: rpc_calls_33.csv
# ==============================================================================

# Import the standard Python csv module to handle reading and parsing CSV files
import csv

# Define a remote procedure 'processData' which takes an amount and returns processed value
def processData(amount):
    # Log the execution of the method on the server with the received parameter
    print("[SERVER] Processing:", amount)
    # Perform arithmetic processing by adding 50 to the received amount and return the result
    return amount + 50

# Define another remote procedure 'checkDonation' that validates eligibility based on amount threshold
def checkDonation(amount):
    # Log the execution of the donation check on the server
    print("[SERVER] Checking donation:", amount)
    # Check if the donation amount meets or exceeds the minimum threshold of 500
    if amount >= 500:
        # Return success message if donation is eligible
        return "Eligible donation"
    # Otherwise, return failure message if donation is below the minimum limit
    return "Below minimum donation"

# Create a dispatch table (dictionary) mapping string procedure names to their corresponding functions
methods = {
    "processData": processData,      # Map string "processData" to the processData function object
    "checkDonation": checkDonation   # Map string "checkDonation" to the checkDonation function object
}

# Open the CSV file containing client RPC requests in read mode with newline='' for proper line handling
with open("rpc_calls_33.csv", "r", newline="") as file:
    # Initialize a CSV reader object to iterate over lines in the file
    reader = csv.reader(file)
    # Skip the first header row (column headers: call_id, client, method_name, parameter)
    next(reader)

    # Iterate through each data row in the CSV file
    for row in reader:
        call_id = row[0]             # Column 0: Unique identifier for the RPC request call
        client = row[1]              # Column 1: Client identifier initiating the remote call
        method_name = row[2]         # Column 2: Name of the remote procedure to be invoked
        parameter = int(row[3])      # Column 3: Argument passed to the procedure, converted to an integer

        # Print the dispatch log showing which client is calling which method with which call ID
        print("\n[DISPATCH]", call_id, client, "invoking", method_name)

        # Verify whether the requested remote method exists in our dispatch dictionary
        if method_name in methods:
            # Dynamically look up the function in the dispatch table and execute it with the parameter
            result = methods[method_name](parameter)
            # Print the server's return value to show successful RPC response
            print("[RETURN] Result:", result)
        else:
            # Handle cases where client requested a procedure that does not exist on the server
            print("[RETURN] Unknown method")
