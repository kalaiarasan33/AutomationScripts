import paramiko

ip='server ip'
user='username'
passw='password'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, port=22, username=user, password=pass)
commands = ["ls -al","df -h"]
for command in commands:
    stdin, stdout, stderr = ssh.exec_command(command)
    outlines=stdout.readlines()
    resp=''.join(outlines)  
    print(resp)
