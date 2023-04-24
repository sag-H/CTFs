import socket
import time
import re


s = socket.socket()         

reg = re.compile('^.+: ([\d]+)\n$')

try:
    port = 10140              

    s.connect(('35.157.111.68', port))

    start_time = time.time()
    print (s.recv(9)) #Read the "Welcome!\n"
    while True:
        msg = (s.recv(1024)).decode("utf-8")
        print (msg)
        match = reg.match(msg)
        if match:
            num = match.group(1)
            print (num)
            s.send(str.encode(num + "\n"))
        else:
            break
    print("--- %s seconds ---" % (time.time() - start_time))
    
            
except:
    raise
finally:
    s.close()