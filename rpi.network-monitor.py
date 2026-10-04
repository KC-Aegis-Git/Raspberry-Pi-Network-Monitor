import subprocess 

ping_times = []

router = "192.168.0.1"

print("Gathering...")

result = subprocess.run(
	["ping", "-c", "10", router],
	capture_output=True,
	text=True
)

for line in result.stdout.splitlines():
	if "time=" in line:
		part = line.split("time=")[1]
		ping_time = float(part.split()[0])
		ping_times.append(ping_time)

mean = sum(ping_times) / len(ping_times)
print('Average ping speed:', mean, 'ms')
