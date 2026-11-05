# EXPERIMENT 8: CRISTIAN'S CLOCK SYNCHRONIZATION
# CSV required: cristian_clocks_32.csv
import csv

with open("cristian_clocks_32.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip headings.

    for row in reader:
        client = row[0]
        t0 = int(row[1])           # Client send time.
        server_time = int(row[2]) # Server time in reply.
        t1 = int(row[3])           # Client receive time.

        rtt = t1 - t0  # Round-trip time.
        estimated_time = server_time + (rtt / 2)  # Estimate one-way delay.
        offset = estimated_time - t1  # Difference from client clock.
        adjusted_time = t1 + offset   # Corrected client time.

        print("\nClient:", client)
        print("RTT:", rtt, "ms")
        print("Estimated Server Time:", estimated_time, "ms")
        print("Clock Offset:", offset, "ms")
        print("Adjusted Time:", adjusted_time, "ms")
