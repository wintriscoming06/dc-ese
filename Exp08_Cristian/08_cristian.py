# ==============================================================================
# EXPERIMENT 8: CRISTIAN'S CLOCK SYNCHRONIZATION ALGORITHM
# Description: Demonstrates external clock synchronization with a time server,
#              accounting for network Round-Trip Time (RTT) delay.
# CSV required: cristian_clocks_32.csv
# ==============================================================================

# Import csv module to parse client and server timing measurements
import csv

# Open the Cristian clock synchronization CSV file in read mode
with open("cristian_clocks_32.csv", "r", newline="") as file:
    # Initialize CSV reader object
    reader = csv.reader(file)
    # Skip the header row (client, t0, server_time, t1)
    next(reader)

    # Iterate through each client synchronization record
    for row in reader:
        client = row[0]             # Column 0: Client name / ID
        t0 = int(row[1])            # Column 1: Time on client clock when request was SENT
        server_time = int(row[2])   # Column 2: Timestamp provided by the time server in response
        t1 = int(row[3])            # Column 3: Time on client clock when response was RECEIVED

        # Calculate Round Trip Time (RTT): total elapsed time measured on client
        rtt = t1 - t0
        # Estimate true server time at moment of arrival assuming symmetric network transit delay (RTT / 2)
        estimated_time = server_time + (rtt / 2)
        # Calculate clock offset: difference between estimated true time and client's receive time
        offset = estimated_time - t1
        # Adjust client clock by adding the calculated offset to synchronize with server
        adjusted_time = t1 + offset

        # Print detailed synchronization report for the client
        print("\nClient:", client)
        print("RTT:", rtt, "ms")
        print("Estimated Server Time:", estimated_time, "ms")
        print("Clock Offset:", offset, "ms")
        print("Adjusted Time:", adjusted_time, "ms")
