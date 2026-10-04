import subprocess 

ping_times = []

router = "192.168.0.1"

print("Gathering...")

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

minimum = min(ping_times)
maximum = max(ping_times)
mean = sum(ping_times) / len(ping_times)

print('- - - - - - - - - - - - - -')
print('Network Monitor (RaspberryPi)')
print(' - - - - - - - - - - - - - ')
print()
print('Router:', status)
print()
print('Maximum ping speed:', maximum, 'ms')
print('Minimum ping speed', minimum, 'ms')
print('Average ping speed:', mean, 'ms')

