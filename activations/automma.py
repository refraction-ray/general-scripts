"""
Tested only on 11.0.1, the welcome message may dependent on the version, but the core is the same
Example: `python3 automma.py '/opt/mma/11.0.1/bin/math'`.
"""
import subprocess
import sys

import mma # see mma.py in the same folder

def autoact(path):
    '''
    param path: string, executable of math
    '''
    x = subprocess.Popen([path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    y = x.communicate()
    mid = y[0].decode("utf-8").split("\n")[11].split("\t")[1]
    passwd = mma.genPassword(mid, "1234-1234-123456")

    x=subprocess.Popen([path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    x.stdin.write(b'\n')
    x.stdin.flush()
    x.stdin.write(b'1234-1234-123456\n')
    x.stdin.flush()
    y = x.communicate(passwd.encode("utf-8"))
    print(y[0].decode("utf-8").split("\n")[-6:-5])

if __name__ == "__main__":
    autoact(sys.argv[1])