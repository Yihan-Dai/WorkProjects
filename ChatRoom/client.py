import socket,select,string #import useful modules
from sys import *


    
if __name__=="__main__":
    if (len(argv)!=3):    # check the input
         print 'Usage:python test.py hostname port'
         exit()
         
    host=argv[1]
    port=int(argv[2])
    
    s=socket.socket()
    try:
        s.connect((host,port)) 
    except:       #Error in connection with server
        print "Unable to connect"
        exit()
        
    print 'Connected to remote host. Start sending messages'
    
    while True:
        socket_list=[stdin,s]
        try:
            rlist,wlist,elist=select.select(socket_list,[],[])
        except:
			s.close()
        
        for sock in rlist: #Loop through each socket in rlist
            if sock==s:
                try:
                    data=sock.recv(1024)
                except:    #Error in socket removal from connections in server
                    print '\nDisconnetced from chat server'
                    exit()
                if not data:  #check the data
                    print '\nDisconnetced from chat server'
                    exit()
                else:
                    stdout.write(data)#output the data from server
                    stdout.flush() ＃make the output flush
            else:
                msg=stdin.readline()  #input the message
                s.send(msg)
                stdout.flush()
    