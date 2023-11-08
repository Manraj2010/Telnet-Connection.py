from netmiko import ConnectHandler
import time
import getpass

# Define the device information
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # The Username is "prne"
    'password': getpass.getpass('Enter Password: '),  # The Password is "cisco123!"
    'secret': getpass.getpass('Enter Enable Password: '),  # Enable password- "Class123!"
    'timeout': 60,  # Setting a longer timeout value helps reduce errors within code
}

# Create a Netmiko SSH session
ssh_session = ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Introduce a delay for stability
time.sleep(2)

# Send a command to change the hostname
new_hostname = 'R2'
config_commands = [f'hostname {new_hostname}']
ssh_session.send_config_set(config_commands)

# Introduce a delay for stability
time.sleep(2)

# Configure a loopback interface
loopback_interface = 'Loopback0'
loopback_ip = '10.0.0.1'
loopback_mask = '255.255.255.255'
config_commands = [f'interface {loopback_interface}',
                   f'ip address {loopback_ip} {loopback_mask}']
ssh_session.send_config_set(config_commands)

# Configure OSPF with a process ID and advertise the loopback interface
ospf_process_id = 1
config_commands = [f'router ospf {ospf_process_id}',
                   f'network {loopback_ip} 0.0.0.0 area 0']
ssh_session.send_config_set(config_commands)

# Introduce a delay for stability
time.sleep(2)

# Send a command to output the running configuration
output = ssh_session.send_command('show running-config')

# Save the running configuration to a file
output_file = 'running_config.txt'
with open(output_file, 'w') as config_file:
    config_file.write(output)

output = ssh_session.send_command('show startup-config')

output_file = 'startup_config.txt'
with open(output_file, 'w') as config_file:
    config_file.write(output)

# Exit enable mode
ssh_session.exit_enable_mode()

# Disconnect from the device
ssh_session.disconnect()

# Display the information
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Enable Password'))
print('{:<20} {:<15} {:<15}'.format(device_info['ip'], device_info['username'], '********'))  # Password is masked
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('--- Loopback interface configured with IP:', loopback_ip)
print('--- OSPF configured to advertise Loopback interface')
print('------------------------------------------------------')
