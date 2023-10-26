from netmiko import ConnectHandler
import pexpect
import getpass

# Define variables
device_ip = '192.168.56.101'
device_username = input('Enter Username: ')  # The Username is "prne"
device_password = getpass.getpass('Enter Password: ')  # The Password is "cisco123!"
enable_password = 'class123!'
output_file = 'running_config.txt'
new_hostname = 'R2'

# Create the SSH session with StrictHostKeyChecking disabled
ssh_session = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {device_username}@{device_ip}', encoding='utf-8', timeout=20)
ssh_result = ssh_session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for SSH session error, if it exists, then display an error and exit
if ssh_result != 0:
    print(f'--- FAILURE! Creating SSH session for: {device_ip}')
    exit()

# Session expecting the SSH password, enter the password
ssh_session.sendline(device_password)
ssh_result = ssh_session.expect(['>', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if ssh_result != 0:
    print(f'--- FAILURE! Entering SSH password: {device_password}')
    exit()

# Enter enable mode
ssh_session.sendline('enable')
ssh_result = ssh_session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if ssh_result != 0:
    print('--- FAILURE! Entering enable mode')
    exit()

# Send enable password details
ssh_session.sendline(enable_password)
ssh_result = ssh_session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])

# Check for error, if it exists then display an error and exit
if ssh_result != 0:
    print('--- FAILURE! Entering enable mode after sending the password')
    exit()

# Send a command to change the hostname using Netmiko
device_info = {
    'device_type': 'cisco_ios',
    'ip': device_ip,
    'username': device_username,
    'password': device_password,
    'secret': enable_password,
    'timeout': 60,
}
netmiko_session = ConnectHandler(**device_info)

config_commands = [f'configure terminal', f'hostname {new_hostname}', 'exit']
netmiko_session.send_config_set(config_commands)

# Send a command to output the running configuration using Netmiko
output = netmiko_session.send_command('show running-config')

# Save the running configuration to a file
with open(output_file, 'w') as config_file:
    config_file.write(output)

# Exit enable mode
netmiko_session.exit_enable_mode()

# Disconnect from the device using Netmiko
netmiko_session.disconnect()

# Terminate SSH session
ssh_session.sendline('exit')
ssh_session.close()

# Display the information within a table
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Password'))
print('{:<20} {:<15} {:<15}'.format(device_ip, device_username, device_password))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('------------------------------------------------------')
