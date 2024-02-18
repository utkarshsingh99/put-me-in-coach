import paramiko
import subprocess


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
        print("Output:", output)
        for i in output.splitlines():
            print(i)
        if error:
            print("Error:", error)

        f = open("results.txt", "w")
        f.write(output.splitlines()[-1])
        f.close()

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
command = 'source ~/put-me-in-coach-venv/bin/activate && cd ~/put-me-in-coach && python ./three_accel_test.py'  # Example command

ssh_execute_command(hostname, port, username, password, command)



remote_user = "pi"  # Replace with the remote username
remote_host = "raspberrypi"  # Replace with the remote host address or IP
remote_file_path = "~/put-me-in-coach/accel_data.csv"  # The full path of the remote file to copy
local_dir = "."  # The local directory to copy the file to, "." denotes the current directory

# Construct the SCP command
scp_command = f"scp {remote_user}@{remote_host}:{remote_file_path} {local_dir}"

result = subprocess.run(scp_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("File copied successfully.")
print(result.stdout.decode())

