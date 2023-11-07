from netmiko import ConnectHandler
import time
import getpass

# Define the device information
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # The Username is "prne"
    'password': getpass.getpass('Enter Password: '),  # The Password is "cisco123!"
    'secret': getpass.getpass('Enter Enable Password: '),  # Enable password
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

# Configure Loopback0 interface with an IP address
loopback0_commands = [
    'interface Loopback0',
    'ip address 192.168.1.1 255.255.255.255',
    'description Loopback0 Interface',
    'no shutdown',
]
ssh_session.send_config_set(loopback0_commands)

# Configure an additional interface (e.g., GigabitEthernet0/0) with an IP address
interface_commands = [
    'interface GigabitEthernet0/0',
    'ip address 192.168.2.1 255.255.255.0',
    'description LAN Interface',
    'no shutdown',
]
ssh_session.send_config_set(interface_commands)

# Configure OSPF
ospf_commands = [
    'router ospf 1',
    'network 192.168.1.1 0.0.0.0 area 0',
    'network 192.168.2.0 0.0.0.255 area 0',
]
ssh_session.send_config_set(ospf_commands)

# Configure EIGRP
eigrp_commands = [
    'router eigrp 100',
    'network 192.168.1.1 0.0.0.0',
    'network 192.168.2.1 0.0.0.0',
]
ssh_session.send_config_set(eigrp_commands)

# Configure RIP
rip_commands = [
    'router rip',
    'version 2',
    'network 192.168.1.1',
    'network 192.168.2.1',
]
ssh_session.send_config_set(rip_commands)

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

# Display the information with messages for OSPF, RIP, and EIGRP configuration on Loopback0
print('------------------------------------------------------')
print('{:<20} {:<15}'.format('Device IP', 'Username'))
print('{:<20} {:<15}'.format(device_info['ip'], device_info['username']))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('--- OSPF, RIP, and EIGRP configuration on Loopback0 completed')
print('------------------------------------------------------')
