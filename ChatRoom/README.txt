{\rtf1\ansi\ansicpg936\cocoartf1348\cocoasubrtf170
{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;}
\paperw11900\paperh16840\margl1440\margr1440\vieww13740\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural

\f0\fs24 \cf0 ================================================================\
This is a simple chat server and client written in Python 2.7.3.\
\
Written by Yihan Dai\
Fall 2015\
\
================================================================\
This programming assignment consists of three parts:\
\
    server.py\
    client.py\
    user_pass.txt\
\
(a) Instructions:\
1. server.py is a server program. It can be invoked as below in the terminal:\
    \
    python server.py <port>\
\
it will create a server socket called welcome socket to listen connections from any client . The variables named (TIME_OUT, LAST_HOUR, BLOCK_TIME) are listed in the main function so that instructors can adjust the values to test the whole program.\
    \
2. client.py is a client program. It can be invoked a shown:\
    \
    python client.py <ip address> <port>\
\
once invoked, a client can be connected with the server. The multi-processes function can ensure many clients simultaneously connected with server. \
\
3. user_pass.txt includes the total nine combinations of username and password. \
    The contents of the textfile is stored into a dictionary called account via make_account() function.\
\
\
(b)  Development environment:\
    \
    This code was written in a UNIX os with Python 2.7.3.\
\
\
(c) Some requirements from assignments:\
    \
    Commands:\
    \
    wholes                                                                   -display all the other users online\
    wholast  <number>                                                -display all the other users online and users who log out within a given time\
    message <user> <message>                                -private message to user\
    broadcast message <message>                           -broadcast message to all the users including yourself\
    broadcast user <user>\'85message <message>    -broadcast message to multiple users\
    logout                                                                    -user log out\
\
\
(d) Output sample:\
    \
     server:\
     \
      
\f1\fs22 \CocoaLigature0 daiyihandeMacBook-Pro:m2 YihanDAI$ python server.py 4119\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural
\cf0    Chat server started at IP:192.168.0.11, Port 4119\
   The server is listening...
\f0\fs24 \CocoaLigature1  \
     \
     client:\
    \
      
\f1\fs22 \CocoaLigature0 daiyihandeMacBook-Pro:m2 YihanDAI$ python client.py 192.168.0.11 4119\
   Connected to remote host. Start sending messages\
   Username> foobar\
   Password> pass\
   You'll have 2 attempts\
   Password> passpass\
   You have logged in!\
   You have entered the room!\
   Do you want to skip the instructions? Y/N \
   --> n\
\
	   Dear foobar, Welcome to use this chat room\
	   I will introduce some commands for you.\
    \
	   "broadcast message <message>"\
	   "broadcast user <user>...message <message>"\
	   "wholast <number>"\
	   "whoelse"\
	   "message <user> <message>"\
	   "logout"\
\
	   Enjoy it! :)\
\
   Command> \
   windows has entered the room!\
   Command> whoelse\
   windows\
\
   Command>   \
   Google has entered the room!\
   Command> whoelse\
   windows\
   Google\
\
   Command> broadcast message why so serious?\
\
   <YOU> why so serious? \
   Command> message windows why so serious?\
\
   Command> broadcast user windows Google message why so serious?\
\
   Command> wholast 1\
   windows\
   Google\
\
   Command> whoelse \
   windows\
\
   Command> message Google hehehehehh\
\
   The user is offline \
   The message is stored..\
   Command> wewewew\
   Wrong Command\
   Command> logout\
   You are logging off\
   Disconnetced from chat server\
   daiyihandeMacBook-Pro:m2 YihanDAI$ }