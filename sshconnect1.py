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

# Loopback interfaces and their IP addresses/subnet masks
loopback_interfaces = ['Loopback0', 'Loopback1', 'Loopback2']
loopback_ips = ['10.0.0.1', '10.0.0.2', '10.0.0.3']
loopback_subnet_masks = ['255.255.255.0', '255.255.255.0', '255.255.255.0']

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

# Configure loopback interfaces with IP addresses and subnet masks
for i in range(len(loopback_interfaces)):
    loopback_commands = [
        f'interface {loopback_interfaces[i]}',
        f'ip address {loopback_ips[i]} {loopback_subnet_masks[i]}',
    ]
    
    ssh_session.send_config_set(loopback_commands)
    time.sleep(2)

# Configure EIGRP to advertise the loopback interfaces
eigrp_commands = [
    'router eigrp 1',  # Assuming you are configuring EIGRP process ID 1
]

for loopback_ip in loopback_ips:
    eigrp_commands.append(f'network {loopback_ip} 0.0.0.0')

ssh_session.send_config_set(eigrp_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure RIP to advertise the loopback interfaces
rip_commands = [
    'router rip',
]

for loopback_ip in loopback_ips:
    rip_commands.append(f'network {loopback_ip}')

ssh_session.send_config_set(rip_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure OSPF to advertise the loopback interfaces
ospf_commands = [
    'router ospf 1',  # Assuming you are configuring OSPF process ID 1
]

for i in range(len(loopback_interfaces)):
    ospf_commands.append(f'network {loopback_ips[i]} 0.0.0.0 area 0')

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
for i in range(len(loopback_interfaces)):
    print(f'--- Loopback interface {loopback_interfaces[i]} configured with IP address: {loopback_ips[i]} and Subnet Mask: {loopback_subnet_masks[i]}')
print('--- EIGRP, RIP, and OSPF configurations applied for Loopback interfaces')
print('------------------------------------------------------')
