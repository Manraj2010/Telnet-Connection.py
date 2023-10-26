import time
import getpass
import telnetlib

# Define the device information
device_info = {
    'ip': '192.168.56.101',
    'username': input('Enter Username: '),  # The Username is "prne"
    'password': getpass.getpass('Enter Password: '),  # The Password is "cisco123!"
}

# Create a Telnet session
tn = telnetlib.Telnet(device_info['ip'])
tn.read_until(b'Username:')
tn.write(device_info['username'].encode('ascii') + b'\n')

# Read the password prompt and send the password
tn.read_until(b'Password:')
tn.write(device_info['password'].encode('ascii') + b'\n')

# Introduce a delay for stability
time.sleep(2)

# Send a command to change the hostname
new_hostname = 'R2'
tn.write(f'configure terminal\n'.encode('ascii'))
tn.write(f'hostname {new_hostname}\n'.encode('ascii'))
tn.write('end\n'.encode('ascii'))

# Introduce a delay for stability
time.sleep(2)

# Send a command to output the running configuration
tn.write('show running-config\n'.encode('ascii'))
output = tn.read_until(b'#', timeout=10).decode('utf-8')

# Save the running configuration to a file
output_file = 'running_config.txt'
with open(output_file, 'w') as config_file:
    config_file.write(output)

# Disconnect from the device
tn.write('exit\n'.encode('ascii'))
tn.close()

# Display the information
print('------------------------------------------------------')
print('{:<20} {:<15}'.format('Device IP', 'Username'))
print('{:<20} {:<15}'.format(device_info['ip'], device_info['username']))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
print('------------------------------------------------------')
