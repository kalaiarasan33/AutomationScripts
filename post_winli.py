from winrm.protocol import Protocol
import paramiko
import hug
import json


@hug.post('/windows',output=hug.output_format.text)
def windows(body):
    print(type(body))
    try:
        host=body['host']
        cmd=body['cmd']
    except:
        host=json.loads(body)['host']
        cmd=json.loads(body)['cmd']

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
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
    return resp

