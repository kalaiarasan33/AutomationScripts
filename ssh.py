import paramiko

ip='server ip'
port=22
username='username'
password='password'

ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip,port,username,password)
commands = ["ls -al","df -h"]
for command in commands:
    stdin, stdout, stderr = c.exec_command(command)
    print (stdout.read())
    print (stderr.read())
