import socket,select,string,time,datetime  #import useful modules
from sys import *
from thread import *     #multi-processes
from threading import Timer #counting time for TIME_OUT


def broadcast_data(sock,username,message): #define a function called broadcast_data() accepting three arguments
    if message[1]=='message': # define 'broadcast message <message>'
        str2=''
        m=2
        while m<len(message):
            str2+=message[m]+' '
            m+=1
        for socket in connect_list:
            if socket !=server_socket:
                if socket!=sock:
                    socket.send("\n\r" + '<' + username + '> ' +str2)
                    socket.send('\nCommand> ')
                else:
                    socket.send("\n\r" + '<' + 'YOU' + '> ' +str2)
    elif message[1]=='user':# define 'broadcast user <user>... message <message>'
        n=2
        global usernames
        while n<len(message):
            if message[n] in account.keys():
                usernames.append(message[n])
            else: 
                break
            n+=1
        n+=1
        str3=''
        while n<len(message):
            str3+=message[n]+' '
            n+=1

        for u in usernames:
            if u in username_list.keys():
                username_list[u].send("\n\r" + '<' + username + '> ' +str3)
                username_list[u].send('\nCommand> ')
            else:
                continue
        usernames=[]
    else:                #broadcast if any user has entered the room
            print message
            for socket in connect_list:
                if socket !=server_socket:
                    if socket!=sock:
                        socket.send(message)
                        socket.send('Command> ')
                    else:
                        socket.send('\nYou have entered the room!')
                
                
                    
def instruction(c,username):   #define the function called instruction() with two arguments
    strin1="""
\tDear %s, Welcome to use this chat room
\tI will introduce some commands for you.
    """%username
    for str in strin1:
        c.send(str,)
        time.sleep(0.08)
        stdout.flush()       #make the output flush
    c.send('\n\t\"broadcast message <message>\"') #commands introduced
    c.send('\n\t\"broadcast user <user>...message <message>\"' )  
    c.send('\n\t\"wholast <number>\"') 
    c.send('\n\t\"whoelse\"')     
    c.send('\n\t\"message <user> <message>\"') 
    c.send('\n\t\"logout\"\n\n')
    time.sleep(0.8)
    strin2='\tEnjoy it! :)\n'
    for str in strin2:
        c.send(str,)
        time.sleep(0.1)
        stdout.flush()    
                
                    
                    
            
def make_account(filename):  #define a function called make_account() with one argument
	account = {}  
	with open("user_pass.txt") as f:    #open the user_pass.txt
		for line in f:
			(name, pwd) = line.split()  #read and split each line into username and password
			account[name] = pwd         #store these in a dictionary called account
	return account
 
def whoelse(sock,username):   #define function whoelse() with two arguments
    for user in username_list.keys():
        if username!=user:
            sock.send(user+'\n')  #show all the other user online

def logout(c,username):      #define logout() with two arguments
    print '%s has logged off' %username
    lgt[username] = datetime.datetime.now()  #store the logout time, pointed at username
    c.send('You are logging off')
    c.close()
    connect_list.remove(c)     #delete the record
    del username_list[username] 

def time_out(sock, username):  #define time_out() with two arguments
	sock.send( '\nUser timed out. Type anything to disconnect.\n') 
	logout(sock, username)           

def auth_pwd(c,pwd,user_name,addr): #define auth_pwd() with four arguments
    attempt=0
    while account[user_name]!=pwd and attempt<2: #check the password attempt
        c.send("You\'ll have %d attempts\nPassword> "%(2-attempt))
        pwd=c.recv(1024)
        pwd=pwd.strip()
        attempt+=1
    if account[user_name]==pwd: 
        c.send('You have logged in!')
        return True
    else:
        lock[user_name]=[datetime.datetime.now(), addr[0]] #record the locke time and address pointing at username
        c.send('Incorrect password. You are locked for ' + str(BLOCK_TIME) + ' seconds.\n')
        return False
        
        
def auth_account(c,addr):   #define auth_account() with two arguments
    c.send("Username> ")
    user_name=c.recv(1024)    #client input the username
    user_name=user_name.strip()
   
    while True:
        if user_name in lock.keys():  #check whether the username is locked
            if lock[user_name][1]==addr[0]:
                time_pass=(datetime.datetime.now() - lock[user_name][0]).total_seconds()
                if time_pass>BLOCK_TIME:
                    pass
                else:                 #Within blocktime
                    c.send('You are still be lock for '+str(BLOCK_TIME-time_pass)+'seconds\n')
                    c.close()
                    connect_list.remove(c)
                    break
       
        if user_name in username_list.keys(): #check the duplicate users
            c.send('You must have logged in, Please use another ID')
            c.send("\nUsername> ")
            user_name=c.recv(1024)
            user_name=user_name.strip()
            
            
        elif user_name in account.keys(): #check if the user in the record
            c.send("Password> ")         #client input the password
            pwd=c.recv(1024)
            pwd=pwd.strip()
            if auth_pwd(c,pwd,user_name,addr)==True: #check the password
                username_list[user_name]=c
                broadcast_data(c,user_name,"\n%s has entered the room!\n" % user_name)
                break
            else:
                print 'a client has been blocked' #three attempts to input password
                c.close()
                connect_list.remove(c)
                break
            
        else:
            c.send("Invalid Username!")     #wrong username
            c.send("\nUsername> ")
            user_name=c.recv(1024)
            user_name=user_name.strip()
    
    return user_name
        
def Command_list(c,addr,username,response):
    if response !='y' and response !='Y': #instructions for this chat room
        instruction(c,username)
    
    if username in offline_txt.keys():    #offline message 
        c.send('\n\nHey, you got a offline message from '+offline_txt[username][0]+' :\n\t')
        offline_msg=offline_txt[username][1]
        for imsg in offline_msg:
            c.send(imsg,)
            time.sleep(0.1)
            stdout.flush()
        del offline_txt[username]
    
    
    
    while True:
        try:
            t=Timer(TIME_OUT,time_out,(c,username,)) #no commands input in the limited time, then logout
            t.start()
            c.send('\nCommand> ')
            command=c.recv(1024)
            t.cancel()
        except :
            if c in connect_list:  #if you type crtl+c,client can gracefully exit
                c.close()
                connect_list.remove(c)
                del username_list[username]
                break
            else:                  #error if user has been locked before
                break
        command=command.rstrip()
        command_list=command.split()  
       
        if command_list==[]:      #no command 
            c.send('None Command')
            continue
        elif command_list[0]=='whoelse':   #show all the other users
            whoelse(c,username)
       
        elif command_list[0]=='wholast':   #show all the other users and users has logout in a given time
            s=int(command_list[1])*60
            if s>0 and s<=LAST_HOUR:
                for all in username_list.keys():
                    if all!=username:
                        c.send(all+'\n')
                for all in lgt.keys():
                    if (datetime.datetime.now()-lgt[all]).total_seconds()<s:
                        c.send(all+'\n')       
       
        elif command_list[0]=='logout':    #logout
            logout(c,username)
            break
        
        elif command_list[0]=='broadcast':  #broadcast message
            broadcast_data(c,username, command_list)
        
        elif command_list[0]=='message':    #private message to one user
            if command_list[1] in username_list.keys():
                for name in username_list.keys():
                    if command_list[1]==name:
                        socket=username_list[name]
                        str1=''
                        i=2
                        while i<len(command_list):
                            str1+=command_list[i]+' '
                            i+=1
                        socket.send("\n\r" + '<' + username + '> ' + str1)
                        if socket!=c:
                            socket.send('\nCommand> ')
            else:
                c.send('\nThe user is offline ')   #user is offline
                c.send('\nThe message is stored..')
                offlinetxt=''
                q=2
                while q<len(command_list):
                    offlinetxt+=command_list[q]+' '
                    q+=1
                offline_txt[command_list[1]]=[username,offlinetxt] #store the message and sender point at the receiver
                
                
                           
        else:   #type any other txt,show wrong message
            c.send('Wrong Command')
            print 'Wrong Command'
            continue

def client(c,addr):
    username=auth_account(c,addr) #validate the client via username and password
    try:    
        c.send('\nDo you want to skip the instructions? Y/N \n--> ') #instruction or not
        response=c.recv(1024)
        response=response.rstrip()
        Command_list(c,addr,username,response) 
    except:    #error if user is locked
        pass
    
                       
if __name__=="__main__":
    connect_list=[]    #connections_list for read via select() function
    account=make_account("user_pass.txt")    #open and read the file into a dictionary
    username_list={}    #once login, store the username and socket
    lgt={}              #once logout, store the username and datetime.now()
    lock={}             #once be locked, store the username, datetime.now() and address
    offline_txt={}      #offline message
    port=int(argv[1])   #port number
    usernames=[]        #this list is for broadcast() function
    BLOCK_TIME = 60
    LAST_HOUR = 3600 
    TIME_OUT =1800 
    
    server_socket=socket.socket()    #initiate the server socket
    host=socket.gethostname()
    server_socket.bind((host,port))
    server_socket.listen(10)
    
    connect_list.append(server_socket) #store the server socket
    
    print "Chat server started at IP:%s, Port %d"%(socket.gethostbyname(host),port)
    time.sleep(0.3)
    print 'The server is listening...'
    
    while True:
        try:
            rlist,wlist,elist=select.select(connect_list,[],[])#Await a read event
        except KeyboardInterrupt:    #type crtl+c, server can gracefully exit
            exit()
        except:
            time.sleep(5) # Error in socket removal from connections
            
        for sock in rlist:      # Loop through each socket in rlist
            if sock==server_socket: #connection request from any client
                csock,addr=server_socket.accept()
                connect_list.append(csock)   #store a client socket
                
                print "Client (%s,%s) has connected" %addr
                start_new_thread(client,(csock,addr)) #for multi_processes
                
      
    server_socket.close()
     