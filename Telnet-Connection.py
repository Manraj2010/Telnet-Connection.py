import pexpect


def telnet_connect(ip_address, username, password):

    try:

        session = pexpect.spawn(f'telnet {ip_address}', encoding='utf-8', timeout=20)


        result = session.expect(['Username:', pexpect.TIMEOUT])


        if result != 0:

            print(f'--- FAILURE! Creating session for {ip_address}')

            return None


        session.sendline(username)

        result = session.expect(['Password:', pexpect.TIMEOUT])


        if result != 0:

            print(f'--- FAILURE! Entering username: {username}')

            return None


        session.sendline(password)

        result = session.expect(['#', pexpect.TIMEOUT])


        if result != 0:

            print(f'--- FAILURE! Entering password: {password}')

            return None


        print('-------------------------------------------------')

        print('')

        print(f'--- Success! Connected to: {ip_address}')

        print(f'--- Username: {username}')

        print(f'--- Password: {password}')

        print('')

        print('---------------------------------')


        return session


    except Exception as e:

        print(f'--- ERROR: {str(e)}')

        return None


def main():

    ip_address = '192.168.56.101'

    username = 'cisco'

    password = 'cisco123!'


    session = telnet_connect(ip_address, username, password)


    if session:

        # Perform additional actions here

        session.sendline('show version')

        session.expect('#')

        print(session.before)  # Print the output of 'show version'

        session.sendline('quit')

        session.close()


if __name__ == "__main__":

    main()