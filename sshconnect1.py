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

# Configure Loopback interfaces with IP addresses and subnet masks
loopback_interfaces = ['Loopback0', 'Loopback1', 'Loopback2']
loopback_ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
subnet_masks = ['255.255.255.255', '255.255.255.255', '255.255.255.255']

ip_commands = []
for i in range(len(loopback_interfaces)):
    ip_commands.extend([
        f'interface {loopback_interfaces[i]}',
        f'ip address {loopback_ips[i]} {subnet_masks[i]}',
    ])

ssh_session.send_config_set(ip_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure EIGRP and advertise the Loopback interfaces
eigrp_commands = [
    'router eigrp 1',  # Assuming you are configuring EIGRP process ID 1
    f'network {loopback_ips[0]} 0.0.0.0',
    f'network {loopback_ips[1]} 0.0.0.0',
    f'network {loopback_ips[2]} 0.0.0.0',
]

ssh_session.send_config_set(eigrp_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure RIP and advertise the Loopback interfaces
rip_commands = [
    'router rip',
    f'network {loopback_ips[0]}',
    f'network {loopback_ips[1]}',
    f'network {loopback_ips[2]}',
]

ssh_session.send_config_set(rip_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure OSPF and advertise the Loopback interfaces
ospf_commands = [
    'router ospf 1',  # Assuming you are configuring OSPF process ID 1
    f'network {loopback_ips[0]} 0.0.0.0 area 0',
    f'network {loopback_ips[1]} 0.0.0.0 area 0',
    f'network {loopback_ips[2]} 0.0.0.0 area 0',
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
print('--- Loopback interfaces configured with IP addresses and subnet masks')
print('--- EIGRP, RIP, and OSPF configurations applied for Loopback interfaces')
print('------------------------------------------------------')
