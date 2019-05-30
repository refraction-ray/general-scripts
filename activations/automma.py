"""
Tested only on 11.0.1 on Ubuntu, the welcome message may dependent on the version, but the core is the same
Example: `python3 automma.py '/opt/mma/11.0.1/bin/math'`.
"""
import subprocess
import sys
import os

import mma # see mma.py in the same folder

def autoact(path=None):
    '''
    param path: string, executable of math
    '''
    if path is None:
        print("math path is not specified, auto detecting...")
        candidates = ["/usr/local/bin/math", "/usr/share/bin/math", "/usr/bin/math", "/opt/Mathematica/bin/math"]
        for p in candidates:
            if os.path.isfile(p):
                print("decided %s as math path"%p)
                path = p
                break
        else:
            print("No math path found, please specify by hand") 
            return 2

    x = subprocess.Popen([path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    y = x.communicate()
    if len(y[0].decode("utf-8").split("\n")) == 5:
        print("Already activated! do nothing.")
        return 1
    mid = y[0].decode("utf-8").split("\n")[11].split("\t")[1]
    passwd = mma.genPassword(mid, "1234-1234-123456")

    x=subprocess.Popen([path], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    x.stdin.write(b'\n')
    x.stdin.flush()
    x.stdin.write(b'1234-1234-123456\n')
    x.stdin.flush()
    y = x.communicate(passwd.encode("utf-8"))
    print(y[0].decode("utf-8").split("\n")[-6:-5])
    return 0

if __name__ == "__main__":
	if len(sys.argv) >= 2:
        autoact(sys.argv[1])
    else:
    	autoact()