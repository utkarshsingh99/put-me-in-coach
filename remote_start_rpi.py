import paramiko

def ssh_execute_command(hostname, port, username, password, command):
    # Initialize the SSH client
    client = paramiko.SSHClient()
    # Automatically add the remote server's SSH key (not recommended for production)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Connect to the remote server
        print("started1")
        client.connect(hostname, port=port, username=username)
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)
        # Read the command output
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print("Error:", error)
        else:
            print("Output:", output)
    except Exception as e:
        print("Connection Failed:", str(e))
    finally:
        # Close the connection
        client.close()

# Example usage
hostname = 'raspberrypi'
port = 22  # default SSH port
username = 'pi'
password = 'pi'
command = 'source ~/put-me-in-coach-venv/bin/activate && python ~/put-me-in-coach/three_accel_test.py'  # Example command

ssh_execute_command(hostname, port, username, password, command)

