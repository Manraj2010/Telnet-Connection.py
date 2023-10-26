# Import the necessary module from netmiko
from netmiko import ConnectHandler
import time

# Set the device parameters
device_ip = '192.168.56.101'
device_username = input('Enter Username: ')
device_password = input('Enter Password: ')
enable_password = 'class123!'
output_file = 'running_config.txt'
new_hostname = 'R2'

# Define the device parameters
device_params = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': device_username,
    'password': device_password,
    'secret': enable_password,
    'verbose': False,
}

# Establish an SSH session with the device
ssh_session = ConnectHandler(**device_params)
ssh_session.enable()

# Sleep for 1 second to ensure proper execution
time.sleep(1)

# Change the hostname of the device
ssh_session.send_command(f'hostname {new_hostname}')
ssh_session.send_command('write memory')

# Sleep for 1 second to ensure proper execution
time.sleep(1)

# Save the running configuration to a file
with open(output_file, 'w') as config_file:
    output = ssh_session.send_command('show running-config')
    config_file.write(output)

# Print the execution details
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Password'))
print('{:<20} {:<15} {:<15}'.format(device_ip, device_username, device_password))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('------------------------------------------------------')

# Close the SSH session
ssh_session.disconnect()