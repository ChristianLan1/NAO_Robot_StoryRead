import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
s.connect((HOST, PORT))
 
s.sendall('Hello, world\n')
time.sleep(5)
s.sendall('Second Sentence\n')
print "Finish sending"