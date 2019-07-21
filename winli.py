
from winrm.protocol import Protocol
import paramiko
from  fire import Fire

def win(host,cmd):
    p = Protocol(
        endpoint="https://{}:5986/wsman".format(host),
        transport='ntlm',
        username=r'Administrator',
        password=r"7q4IBD5@wMozcG?O?per5HDEcvnBVE%%",
        server_cert_validation='ignore')

    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, cmd)
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    outlines = std_out.decode("utf-8")
    resp = "".join(outlines)
    print(resp)
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)



def li(host,cmd):
    username = "kalai"
    passw="kalai"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username , password=passw)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    outlines = stdout.readlines()
    resp = "".join(outlines)
    print(resp)

if __name__=="__main__":
    Fire()
