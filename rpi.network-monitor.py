import subprocess 

router = "192.168.0.1"

result = subprocess.run(
	["ping", "-c", "10", router],
	capture_output=True,
	text=True
)

print(result.stdout)
