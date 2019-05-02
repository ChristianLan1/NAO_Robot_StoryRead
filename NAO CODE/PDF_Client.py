import socket
import time
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

class client:
    def __init__(self):
        self.clientSocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def connection(self):
        
        #now connect to the web server on port 5555
        try:
            self.clientSocket.connect((HOST, PORT))
            print "connection est"
            return True
        except socket.error:
            return False
    def turnPage(self):

        self.clientSocket.sendall('Turn\n')
        print "Finish sending"