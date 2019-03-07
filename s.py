import socket
import threading, Queue
from time import gmtime, strftime
import time


HOST = '127.0.0.1'        
PORT = 50007              
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

currentConnections = list()
  
    
# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = "" 
roomTitle = ""  

# custom say hello command
def sayHello():
    print "----> The hello function was called"
    

# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a 
# command it will then need to extract the command.
def parseInput(data, con):
    print "parsing..."
    print str(data)
    
    # Checking for commands 
    if "/getservertime" in data:
        print "command in data.."
        formatted= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        
        con.send(str(formatted))
    
    if "/sayHi" in data:
        con.send(str("Hi there!"))
        
    if "/getRoomTitle" in data:
        print "Fetching title of room..."
        con.send(str(roomTitle))
    
    if "/closeServer" in data:
        s.close()
        
    if "%USERNAME:" in data:
        con.send(str("This does nothing for now"))
    
# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.
    
def manageConnection(conn, addr):
    global buffer
    global currentConnections
    print 'Connected by', addr
    
    currentConnections.append(conn)
    
    
    while 1:    
        data = conn.recv(1024)
        
        parseInput(data,conn)# Calling the parser
        
        print "rec:" + str(data)
        
        for singleClient in currentConnections:
            singleClient.send(str(data))
       
            
    #conn.close()

print "Enter name of chatroom:"
roomTitle = raw_input()
    
while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))
    
    t.start()
    
    


