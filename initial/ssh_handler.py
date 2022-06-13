import paramiko
import re


class SecureShellHandler:

    def __init__(self, host, user, psw):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, password=psw, port=22, timeout=5)

        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def execute(self, cmd):
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of buffer'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                shout = []
            elif str(line).startswith(finish):
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    sherr = shout
                    shout = []
                break
            else:
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))
        shout = (i for i in shout if "\x00" not in i)
        sherr = (i for i in sherr if "\x00" not in i)
        return shin, shout, sherr
