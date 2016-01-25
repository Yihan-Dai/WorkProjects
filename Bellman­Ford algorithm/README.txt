==========================================================================================
This is a simple version of the distributed Bellman­Ford algorithm written in Python 2.7.3.

Written by Yihan Dai
DEC,23 2015

==========================================================================================
This programming assignment consists of two parts:
     
     bfclient.py
     README.txt

(a) Instructions
   (1)The requirements of coursework:
      It requires that the algorithm should be operated using a set of distributed client processes. Each clients perform the distributed 
      distance computation and support a user interface, e.g., it allows the user to edit links to the neighbors and view the routing table. 
      Clients may be distributed across different machines and more than one client can be on the same machine.
   (2) The bfclient.py should be invoked as below in the terminal:
      python bfclient.py <listening-port> <timeout> <ip-address1 port1 distance1> <ip-address2 port2 distance2> ...

(b) Usage scenario
   (1) Start one node:
       -$ python bfclient.py 10001 4 
       
       This will establish a UDP Socket where ip address is localhost and port number is 10001
   (2) Start one node with one edge:
       -$ python bfclient.py 10000 4 localhost(or the other ip address) 10001 13.2 
       
       This will establish another UDP Socket where ip address is local host and port number is 10000. It can connect actively with the above node and exchange the vector table after the connection.
   (3) Start with one node with two or more edges:
       -$ python bfclient.py 10000 4 localhost(or the other ip address) 10001 13.2 local host 10002 14.3
       
       Firstly, it will create a node with two edges. And once it is established, it will broadcast its vector table to the two neighbors. And if there is no reply or either of neighbor is not set within the three times of the interval, in this case, which is 12s, then the node will deny the neighbors and close their connections.

#####You can try it via the triangle topology or the more complex design.

(c) Program features
   (1) SHOWRT 

A neighbor is requesting the connection
-$ SHOWRT
------------------------------------------------------------------------------
Dec-23-2015, 08:14 PM, 44 seconds
Distance vector list is:
Destination = 192.168.0.7:20002, Cost = 14.0, Link = (192.168.0.7:20002)
Destination = 192.168.0.7:20001, Cost = 27.0, Link = (192.168.0.7:20002)
------------------------------------------------------------------------------
    
   (2) LINKDOWN You can use it as shown below.
       LINKDOWN 192.168.0.7 20002
        
-$ LINKDOWN 192.168.0.7 20002
SHOWRT
------------------------------------------------------------------------------
Dec-23-2015, 08:17 PM, 12 seconds
Distance vector list is:
Destination = 192.168.0.7:20002, Cost = inf, Link = ()
Destination = 192.168.0.7:20001, Cost = inf, Link = ()
------------------------------------------------------------------------------

   (3) lINKUP the previous link
       LINKDOWN 192.168.0.7 20002
-$ LINKUP 192.168.0.7 20002
SHOWRT
------------------------------------------------------------------------------
Dec-23-2015, 08:18 PM, 29 seconds
Distance vector list is:
Destination = 192.168.0.7:20002, Cost = 14.0, Link = (192.168.0.7:20002)
Destination = 192.168.0.7:20001, Cost = 27.0, Link = (192.168.0.7:20002)
------------------------------------------------------------------------------

   (4) CLOSE
       Type the “CLOSE” command in the line. It will make the node closed and send to its neighbors that the distance between itself and them should be set as infinity. 

(d) Extra features
   
   (1) SHOWNEIGHBOR
-$ SHOWNEIGHBOR
------------------------------------------------------------------------------
Dec-23-2015, 08:22 PM, 21 seconds
The node's neighbors are:
Neighbor = 192.168.0.7:20002
------------------------------------------------------------------------------
   
   (2) LINKCHANGE
       It can used to change the link cost between one node with any of its neighbors.
Methods:

LINKCHANGE 192.168.0.7 20002 9
SHOWRT
------------------------------------------------------------------------------
Dec-23-2015, 08:24 PM, 16 seconds
Distance vector list is:
Destination = 192.168.0.7:20002, Cost = 9.0, Link = (192.168.0.7:20002)
Destination = 192.168.0.7:20001, Cost = 22.0, Link = (192.168.0.7:20002)
------------------------------------------------------------------------------

(d) Protocol
   
   (1) In the code, i try to use the json which is called (JavaScript Object Notation) to encode the data needed to be sent to the node’s neighbors. 
    JSON (JavaScript Object Notation), specified by RFC 7159 (which obsoletes RFC 4627) and by ECMA-404, is a lightweight data interchange format inspired by JavaScript object literal syntax (although it is not a strict subset of JavaScript).
    In detail, i used the method which is named json.dumps() to make the string into the unicode. And then the “unicode” data will be transferred to another UDP socket, where it should be loaded by the method “son.loads()” afterwards. 
    The data is a dictionary which includes the type of the command, the node’s vector table consisting of the distance between itself and other nodes, and the direct link cost between itself and receiver.
    The sending data is given below as an example:

{u'load': {u'costs': {u'192.168.0.7:20002': 0.0, u'192.168.0.7:20001': 13.0, u'192.168.0.7:20004': 14.0}, u'neighbor': {u'direct': 14.0}}, u'type': u'update_cost'}
    
   (2) Syntax 
     JSON syntax is basically considered as a subset of JavaScript syntax; it includes the following:

1. Data is represented in name/value pairs.

2. Curly braces hold objects and each name is followed by ':'(colon), the name/value pairs are separated by , (comma).

3. Square brackets hold arrays and values are separated by ,(comma).

     One example is given:

{
   "book": [
	
      {
         "id":"01",
         "language": "Java",
         "edition": "third",
         "author": "Herbert Schildt"
      },
		
      {
         "id":"07",
         "language": "C++",
         "edition": "second"
         "author": "E.Balagurusamy"
      }
		
   ]
}

    JSON supports the following two data structures 

1. Collection of name/value pairs − This Data Structure is supported by different programming languages.

2. Ordered list of values − It includes array, list, vector or sequence etc.

(e) Any possible bugs
    The timeout is used for the node to send the message to other neighbors. And if the time exceeds 3xTimeout_interval, then it will ignore the neighbor who does not give a reply to the node in time.
    However, in one case that if i want to create a node with one edge, and another node could not be established in the 3xTime_Interval, then there will be no connection between the two nodes. Maybe another operation can ignore this.
