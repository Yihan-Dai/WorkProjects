'''
The file is created by Yihan Dai on DEC 23, 2015.
The operating system is OSx and python 2.7.10 is used.
'''

import socket,select,json
import sys,time
from collections import defaultdict
from threading import Thread, Timer
from datetime import datetime
Orign_argv = {}
commandList = ['SHOWRT','SHOWNEIGHBOR','CLOSE','LINKDOWN','LINKUP','LINKCHANGE' ] #all commands list
changeList = ['LINKDOWN','LINKUP','LINKCHANGE']	 #a list including linkdown,linkchange and linkup

class RepeatTimer(Thread):	#thread that will call a function every interval seconds
	
	def __init__(self, interval, target):
		Thread.__init__(self)
		self.target = target
		self.interval = interval
		self.daemon = True
		self.stopped = False
	def run(self):
		while not self.stopped:
			time.sleep(self.interval)
			self.target()

class ResettableTimer(): #close the connection if no reply within 3xinterval
	def __init__(self, interval, func, args=None):
		self.interval = interval
		self.func = func
		self.args = args
		self.countdown = self.create_timer()
	def start(self):
		self.countdown.start()
	def reset(self):
		self.countdown.cancel()
		self.countdown = self.create_timer()
		self.start()
	def create_timer(self):
		t = Timer(self.interval, self.func, self.args)
		t.daemon = True
		return t
	def cancel(self):
		self.countdown.cancel()


def checkint(port): #check the port number
	try:
		int(port)
		return True
	except ValueError:
		return False

def checknum(number): #check the link cost
	try:
		float(number)
		return True
	except ValueError:
		return False
		
def addr2key(host, port):  #change the format of the address and the port number
	if host == 'localhost':
		host = socket.gethostbyname(socket.gethostname())
	return "{0}:{1}".format(host, port)

def create_vector(cost=None, neighbor_set=None , direct = None, route= None,costs = None):
	vector = default_vector() #create a vector table
	vector['cost'] = cost
	vector['neighbor_set'] = neighbor_set
	vector ['direct'] = direct if direct !=None else float("inf")
	vector ['costs'] = costs if costs != None else defaultdict(lambda: float("inf"))
	vector['route'] = None
	if neighbor_set:
		vector['route'] = route
		monitor = ResettableTimer( #call the linkdown method if no reply from that neighbor
			interval = 3*dict['timelast'], 
			func = linkdown,
			args = list(tupleAddress(route)))
		monitor.start()
		vector['silence_monitor'] = monitor
	return vector
	
def check_argv(argu): # check the user's input
	if (len(sys.argv)%3) == 0:
		print "input is correct"
	Listen_port = argu.pop(0)
	if checkint(Listen_port):
		Orign_argv['port'] = Listen_port
	else:
		print "error"
		sys.exit(0)
	Time_interval = argu.pop(0)
	if checknum(Time_interval):
		Orign_argv['timelast'] = float(Time_interval)
	else:
		print "error"
		sys.exit(0)
	Orign_argv['neighbors'] = []
	Orign_argv['costs'] = []
	while len(argu) >= 3:
		address = argu[0]
		port = argu[1]
		Orign_argv['neighbors'].append(addr2key(address, port))
		cost = argu[2]
		Orign_argv['costs'].append(float(cost))
		#print argu[0:3]
		del argu[0:3]
	return Orign_argv

def default_vector(): #one default vector table
	return { 'route' :None , 'cost' : float('inf'), 'neighbor_set' : False}		   
 
def tupleAddress(addr):	 # pack the address and port number into tuple
	host,port = addr.split(':')
	return host,int(port)
 
def sendMessage(): #send data to other neighbors
	
	sendCosts={keys:values['cost']for keys, values in vectors.iteritems()}	 
	sendData = { 'type': 'update_cost'}
	for keys, values in vectors.iteritems():
		if values['neighbor_set']:
			sendData['load'] = { 'costs': sendCosts}
			sendData['load']['neighbor'] = { 'direct': values['direct'] }
			Server_socket.sendto(json.dumps(sendData), tupleAddress(keys))
			#print tupleAddress(keys)

def updateCost(): #receive the vector table from neighbor, then update the cost
	neighborHost,neighborPort = sender
	neighborAddr = addr2key(neighborHost,neighborPort)
	receivedCosts = loadData['costs']

	for key in receivedCosts:
		if key not in vectors.keys():
			vectors[key] = default_vector()
	if not vectors[neighborAddr]['neighbor_set']:
		print 'A neighbor is requesting the connection'
		del vectors[neighborAddr]
		
		vectors[neighborAddr] = create_vector(
		 cost = float('inf'),
		 costs = receivedCosts,
		 route = neighborAddr,
		 neighbor_set = True,
		 direct = loadData['neighbor']['direct'])
		 
	else :
		vectors[neighborAddr]['costs'] = receivedCosts
		vectors[neighborAddr]['silence_monitor'].reset()
	getCost()
	
def getCost(): # A BELLmanFord algorithm
	for TargetAddr, TargetInfo in vectors.items():
		if TargetAddr != selfvector:
			cost = float("inf")
			nexthop = ''
			for keys, values in vectors.items():
				if values['neighbor_set']:
					if TargetAddr in values['costs']:
						shortest = values['direct'] + values['costs'][TargetAddr]
						if shortest < cost:
							cost =shortest
							nexthop = keys
			TargetInfo['cost'] = cost
			TargetInfo['route'] = nexthop

def check_message(message): #check the message from sys.stdin
	message = message.strip('\n')
	message = message.split(' ')
	if message[0] not in commandList:
		return 'Error: The command is invalid!'
	if message[0] in changeList:
		if message[0] == 'LINKCHANGE':
			if len(message) == 4 and checkint(message[2]) and checknum(message[3]):
				message[0] = message[0].lower()
				return message
			else:
				return 'Error: \'LINKCHANGE\' is not called by your arguments'
		elif len(message) > 3:
			return 'Error: Destination address is incorrect!'
		
		if checkint(message[2]):
			message[0] = message[0].lower()
			return message
	else:
		message[0] = message[0].lower()
		return message
		
		
def showrt(): #showrt command
	print '-'*78
	print datetime.now().strftime("%b-%d-%Y, %I:%M %p, %S seconds")
	print "Distance vector list is:"
	for keys, values in vectors.items():
		if keys != selfvector:
			print ("Destination = {destination}, "
				   "Cost = {cost}, "
				   "Link = ({nexthop})").format(
						destination = keys,
						cost		= values['cost'],
						nexthop		= values['route'])
	print '-'*78# extra line

def show_neighbors(): #showneighbor command
	print '-'*78
	print datetime.now().strftime("%b-%d-%Y, %I:%M %p, %S seconds")
	print 'The node\'s neighbors are:'
	count = 0
	for keys,values in vectors.items():
		if values['neighbor_set']:
			count +=1
	if count == 0:
		print "There's no neighbor for this node"
		return 
	for keys, values in vectors.items():
		if values['neighbor_set']:
			print 'Neighbor = {0}'.format(keys)
	print '-'*78

def linkdown(host,port): #linkdown command 
	neighborAddr = addr2key(host,port)
	if neighborAddr not in vectors:
		print'Error: No such kind of node'
		return
	vector = vectors[neighborAddr]
	if not vector['neighbor_set']:
		print 'Error: No such kind of neighbor'
		return 
	vector['saved'] = vector['direct']
	vector['direct'] = float("inf")
	vector['neighbor_set'] = False
	vector['silence_monitor'].cancel()
	getCost()

def linkup(host,port): #linkup command
	neighborAddr = addr2key(host,port)
	vector = vectors[neighborAddr]
	if 'saved' not in vector:
		print 'Not this target'
		return
	vector['direct'] = vector['saved']
	vector['neighbor_set'] = True
	del vector['saved']
	getCost()

def linkchange(host,port,cost): #linkchange commad
	neighborAddr = addr2key(host,port)
	if neighborAddr not in vectors:
		print'Error: No such kind of node'
		return
	vector = vectors[neighborAddr]
	if not vector['neighbor_set']:
		print 'Error: No such kind of neighbor'
		return 
	if 'saved' in vector:
		print 'This link has been shut down by LINKDOWN cmd'
		return
	if cost < 1:
		print 'The direct cost should be more than 1'
		return
	vector['direct'] = cost
	getCost()
	
def close(): #close command
	print 'The node has been closed...Take care!'
	sys.exit(0)
	
def sendData(command,load = None): #send datd to udp socket
	if load == None:
		load = {}
	data = json.dumps({ 'type': command[0], 'load': load })
	Tport = int(command[2])
	Thost = command[1]
	Server_socket.sendto(data, (Thost,int(Tport)))
	return Thost,Tport

if __name__ =='__main__':
	Arguments = sys.argv[1:]
	dict = check_argv(Arguments)


	host = socket.gethostbyname(socket.gethostname()) 
	Listen_port = int(dict['port'])
	
	Server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# establish a node
	try:
		Server_socket.bind((host, Listen_port))
		print "listening on {0}:{1}\n".format(host,Listen_port)
	except socket.error, msg:
		print "an error occured binding the server socket. \
			   error code: {0}, msg:{1}\n".format(msg[0], msg[1])
		sys.exit(1)
	
	vectors = defaultdict(lambda:default_vector)
	
	s = zip(dict['neighbors'],dict['costs'])
	
	for neighbor, cost in s: #establish the vector table
		vectors[neighbor] = create_vector(cost = cost,neighbor_set = True, route = neighbor, direct = cost)
	
	selfvector = addr2key(host,Listen_port)
	vectors[selfvector] = create_vector(cost = 0.0,neighbor_set = False, route = addr2key(host, Listen_port),direct = 0.0)
	
	
	sendMessage()
	RepeatTimer(dict['timelast'], sendMessage).start() #call the thread that every interval, send the vector table
	#Server_socket.sendto('wwwww',(host,20001)) 
	connect_list=[Server_socket,sys.stdin]
	
	while True:
		try:
			rlist,wlist,elist=select.select(connect_list,[],[])#Await a read event
		except KeyboardInterrupt:	 #type crtl+c, server can gracefully exit
			sys.exit(0)
		except:
			time.sleep(5) # Error in socket removal from connections
		
		for sock in rlist: #listen to other sockets 
			if sock == Server_socket:
				data, sender = sock.recvfrom(1024)	  
				received = json.loads(data)
				loadData = received['load']
				type = received['type']
				if type == 'update_cost':
					updateCost()
				elif type == 'linkdown':
					linkdown(*sender)
				elif type == 'linkup':
					linkup(*sender)
				elif type == 'linkchange':
					linkchange(*sender,cost=loadData['direct'])
			
			if sock == sys.stdin: #listen to the user input
				message = sock.readline()
				command = check_message(message)
				if command[0] == 'showrt':
					showrt()
				elif command[0] == 'showneighbor':
					show_neighbors()
				elif command[0] == 'close':
					close()
				elif command[0] == 'linkchange':
					cost = float(command[3])
					Thost, Tport = sendData(command = command, load = {'direct': cost})
					linkchange(Thost, Tport, cost)
				elif command[0] == 'linkdown':
					Thost, Tport = sendData(command = command)
					linkdown(Thost,int(Tport))
				elif command[0] == 'linkup':
					Thost, Tport = sendData(command = command)
					linkup(Thost,int(Tport))
				else:
					print command