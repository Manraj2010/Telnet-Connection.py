import telnetlib
import time

# Define variables
ip_address = "192.168.56.101"
username = input('Enter Username: ')  # The username is "cisco"
password = input('Enter Password: ')  # The password is "cisco123!"
new_hostname = "R2"
config_file = "running_config.txt"
loopback_ip = "10.0.0.1"  # Loopback IP address
subnet_mask = "255.255.255.255"  # Subnet mask

# EIGRP and RIP configurations
eigrp_as_number = 100
rip_network = "192.168.1.0"
rip_version = "2"

# Create a Telnet session
tn = telnetlib.Telnet(ip_address)

try:
    # Read the initial prompt and wait for login
    tn.read_until(b"Username: ", timeout=5)
    tn.write(username.encode('ascii') + b"\n")

    # Wait for password prompt and enter the password
    tn.read_until(b"Password: ", timeout=5)
    tn.write(password.encode('ascii') + b"\n")

    # Waiting for the prompt and then a delay happens
    time.sleep(2)
    tn.read_very_eager()

    # Send a command to configure the hostname
    tn.write(b"configure terminal\n")
    tn.read_until(b"#", timeout=5)

    tn.write(f"hostname {new_hostname}\n".encode('ascii'))
    tn.read_until(b"#", timeout=5)

    # Configure loopback interface
    tn.write(b"interface Loopback0\n")
    tn.read_until(b"#", timeout=5)
    tn.write(f"ip address {loopback_ip} {subnet_mask}\n".encode('ascii'))
    tn.read_until(b"#", timeout=5)

    # Configure EIGRP for loopback
    tn.write(b"router eigrp " + str(eigrp_as_number).encode('ascii') + b"\n")
    tn.read_until(b"#", timeout=5)
    tn.write(b"network " + loopback_ip.encode('ascii') + b" 0.0.0.0\n")
    tn.read_until(b"#", timeout=5)

    # Configure RIP for loopback
    tn.write(b"router rip\n")
    tn.read_until(b"#", timeout=5)
    tn.write(b"version " + rip_version.encode('ascii') + b"\n")
    tn.read_until(b"#", timeout=5)
    tn.write(b"network " + rip_network.encode('ascii') + b"\n")
    tn.read_until(b"#", timeout=5)
    
    # Save the modified running configuration to the device
    tn.write(b"end\n")
    tn.read_until(b"#", timeout=5)
    tn.write(b"write memory\n")
    tn.read_until(b"#", timeout=5)

    # Read the running configuration
    tn.write(b"show running-config\n")
    running_config = tn.read_until(b"#", timeout=60).decode('ascii')

    # Save the running configuration to a local file
    with open(config_file, "w") as f:
        f.write(running_config)

    # Display success message
    print("-------------------------------------------------")
    print("        Telnet Configuration Script")
    print("-------------------------------------------------")
    print(f"Device IP: {ip_address}")
    print(f"Username: {username}")
    print("Password: ******")
    print(f"Hostname changed to: {new_hostname}")
    print(f"Loopback IP configured: {loopback_ip}")
    print(f"EIGRP configuration applied (AS {eigrp_as_number})")
    print(f"RIP configuration applied (Network {rip_network})")
    print(f"Running configuration saved to: {config_file}")
    print("-------------------------------------------------")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the Telnet session
    tn.close()
