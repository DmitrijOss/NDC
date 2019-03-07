import threading
# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def readInputThreaded(so):
    while 1:
        print "Please enter your name:"
        name = raw_input()

        print "Enter your message:"
        text = raw_input()

        if "/closeConnection" in text:
            s.close()
    
        so.sendall(str(text))

t = threading.Thread(target=readInputThreaded, args = (s,))
t.start()
# when we send data to the server, we are using a colon
# at the end of a sentence to mark the end of the current sentence
# later when the input comes back, we will then be breaking the input
# into individual parts using the colon : to separate the lines
#s.sendall("%USERNAME:"+name)

'''
Thread to read from the server 
'''
def readFromServer(s):
   
    while 1:
        data = s.recv(100)
      
        print "Response:" + str(data) + '\n'
        


t = threading.Thread(target=readFromServer, args = (s,))
t.start()
