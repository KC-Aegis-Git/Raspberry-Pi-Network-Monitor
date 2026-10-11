# THIS DOES NOT MONITOR A WHOLE NETWORK.
# It only measures SOME network statistics from the device this script is running on, such as latency.
# This was made with a Raspberry Pi in mind, but it works on any device running Linux that is also connected to a network.

import subprocess
import time
import sys

def detect_router():
    result = subprocess.run(
        ["ip", "route", "show", "default"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error: Unable to detect default gateway: IP route failed.")
        sys.exit(1)

    for line in result.stdout.splitlines():
        if line.startswith("default via "):
            parts = line.split()
            return parts[2]

    print("Error: No default gateway was found on this device.")
    sys.exit(1)

router = detect_router()

print("Gathering...")

while True:
    ping_times = []

    result = subprocess.run(
        ["ping", "-c", "10", router],
        capture_output=True, # Does not immediately print
        text=True
    )

    if result.returncode == 0:
        status = 'ONLINE'
    else:
        status = 'OFFLINE'

    for line in result.stdout.splitlines():
        if "time=" in line:
            part = line.split("time=")[1]
            ping_time = float(part.split()[0])
            ping_times.append(ping_time)

    packets_sent = 10
    packets_received = len(ping_times)

    packet_loss = ((packets_sent - packets_received) / packets_sent) * 100

    if ping_times == []:
        minimum = "N/A"
        maximum = "N/A"
        mean = "N/A"
    else:
        minimum = min(ping_times)
        maximum = max(ping_times)
        mean = sum(ping_times) / len(ping_times)

    subprocess.run(["clear"])

    print('- - - - - - - - - - - - - -')
    print('Network Monitor (RaspberryPi)')
    print(' - - - - - - - - - - - - - ')

    print()
    print('Router:', status)
    print()
    print('Maximum ping speed:', maximum, 'ms')
    print('Minimum ping speed', minimum, 'ms')
    print('Average ping speed:', mean, 'ms')
    print()
    print('Packet loss:', packet_loss, '%')
    print('(Sent', packets_sent, 'packets)')
    print()

    time.sleep(5)
