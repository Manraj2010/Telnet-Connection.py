from netmiko import ConnectHandler
import time

# Define the device information
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': input('Enter Username: '),  # The Username is "prne"
    'password': input('Enter Password: '),  # The Password is "cisco123!"
    'secret': 'class123!',  # Enable password
    'timeout': 60,  # Set a longer timeout value (adjust as needed)
}

# Create a Netmiko SSH session
ssh_session = ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Introduce a delay for stability (optional)
time.sleep(2)

# Send a command to change the hostname
new_hostname = 'R2'
config_commands = [f'hostname {new_hostname}']
ssh_session.send_config_set(config_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure a loopback interface
loopback_commands = [
    'interface Loopback0',
    'ip address 10.0.0.1 255.255.255.255',
]
ssh_session.send_config_set(loopback_commands)

# Configure EIGRP
eigrp_commands = [
    'router eigrp 100',  # Use your desired EIGRP AS number
    'network 10.0.0.1 0.0.0.0',  # Advertise the loopback network
]
ssh_session.send_config_set(eigrp_commands)

# Configure RIP
rip_commands = [
    'router rip',
    'version 2',
    'network 192.168.1.0',
]
ssh_session.send_config_set(rip_commands)

# Configure OSPF
ospf_commands = [
    'router ospf 1',  # Use your desired OSPF process ID
    'network 10.0.0.1 0.0.0.0 area 0',  # Advertise the loopback network in OSPF Area 0
]
ssh_session.send_config_set(ospf_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Send a command to output the running configuration
output = ssh_session.send_command('show running-config')

# Save the running configuration to a file
output_file = 'running_config.txt'
with open(output_file, 'w') as config_file:
    config_file.write(output)

# Exit enable mode
ssh_session.exit_enable_mode()

# Disconnect from the device
ssh_session.disconnect()

# Display the information
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Password'))
print('{:<20} {:<15} {:<15}'.format(device_info['ip'], device_info['username'], device_info['password']))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('--- Loopback and interfaces configured with EIGRP, RIP, and OSPF')
print('------------------------------------------------------')

