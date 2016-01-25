'''
The file is created by Yihan Dai on Nov 9, 2015.
The operating system is OSx and python 2.7.10 is used.
'''
import sys 
import socket
import struct
import time
from time import strftime
Max_segement = 576    #MSS the maximum segement
ACK_ack = 0          #the ack number from receiver to sender
ACK_sequence = 0     #sequence number from receiver to sender

def varify_check(header_str):   #validate the checksum
    "To calculate the checksum part"
    sum_calc = 0
    

    #Divide the string by 16 bits and calculate the sum
    for num in range(len(header_str)):
        if num % 2 == 0:     # Even parts with higher order
            sum_calc = sum_calc + (ord(header_str[num]) << 8)
        elif num % 2 == 1:   # Odd parts with lower order
            sum_calc = sum_calc + ord(header_str[num])
    
    # Get the inverse as the checksum
    outputsum = (sum_calc % 65536)                       
    
    return outputsum

def wrto_file(writefile,received):   #write the file into the write.txt
    Datafile = open(writefile,"a") 
    Datafile.write(received[8])
    print received[8]
    Datafile.close()

def logwriting(segment_num, direction, timestamp, source, destination, sequence_num, ACK_num, ackflag, finflag, trans_status):
    #write the logfile after receiving the different ack from receiver
    
    #Determine the writing direction     
    if direction == 'forward':
        logdirection = 'Sender -> Receiver'
    elif direction == 'backward':
        logdirection = 'Receiver -> Sender'
    else:
        logdirection = direction
    
    #Log line format     
    logline = str(segment_num).ljust(10) + logdirection.ljust(20) + timestamp.ljust(22) + source.ljust(15) + destination.ljust(15) + str(sequence_num).ljust(11) + \
              str(ACK_num).ljust(7) + str(ackflag).ljust(5) + str(finflag).ljust(5) + trans_status.ljust(8) + '\r\n'
    
    #Check the output method (stdout or write to a log file)   
    if log_filename == 'stdout.txt':
        print logline
    else:
        try:
            logfile = open(log_filename, "a")
        except:
            print 'Unable to open file'
        logfile.write(logline)
        logfile.close()
    
    return


if __name__ == '__main__':
	
    UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     #establish a UDP socket to listen from any data from sender   
    UDP_HOST = socket.gethostbyname(socket.gethostname())
    UDP_PORT = int(sys.argv[2])
    writefile = sys.argv[1] #accept the arguments
    sender_IP = sys.argv[3]
    log_filename = sys.argv[5]
    try:
        UDPsocket.bind((UDP_HOST, UDP_PORT)) #print the error messages
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
    print 'The ip address is : %s' %socket.gethostbyname(socket.gethostname())
    print 'Waiting for the packet'
    UDPrecdata = UDPsocket.recvfrom(596*5) 
    received = struct.unpack('!HHIIHHHH%ds'%(len(UDPrecdata[0])-20), UDPrecdata[0]) #receive the data and unpack it
    logwriting('Segment#', 'Trans_direction', 'Timestamp', 'Source', 'Destination', 'Sequence#', 'ACK#', 'ACK', 'FIN', 'Trans_status')
    sum_output = varify_check(UDPrecdata[0]) #checksum
    window_size = received[5]
    if received[4] == 0:    #determine the different ack and fin flags
        ackflag = 0
        finflag = 0
    elif received[4] == 1:
        ackflag = 0
        finflag = 1
    elif received[4] == 16:
        ackflag = 1
        finflag = 0
    elif received[4] == 17:
        ackflag = 1
        finflag = 1
    
    if sum_output == 65535:  #confirm whether the packet is corrupted
        print 'The packet is uncorrupted'
        wrto_file(writefile,received) #write to the file and log file
        logwriting((int(received[2]) / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), sender_IP, UDP_HOST, received[2], received[3], ackflag, finflag, 'Received')
    else: 
        print 'The packet is corrupted'
        logwriting((int(received[2]) / (Max_segement*window_size)+ 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), sender_IP, UDP_HOST, received[2], received[3], ackflag, finflag, 'Dropped')
    
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     #connect to sender via a TCP socket
    TCP_HOST = sys.argv[3]
    TCP_PORT =  int(sys.argv[4])
    TCPsocket.connect((TCP_HOST, TCP_PORT))
    if sum_output == 65535:# if the packet is uncorrupted, send a ack including a next packet number
        ACK_ack = received[2] + (len(UDPrecdata[0])-20)
        TCPsocket.send(str(ACK_sequence) + ',' + str(ACK_ack)) 
        logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), UDP_HOST , sender_IP, 0,ACK_ack , ackflag, finflag, 'Succeed')        
    else: 
        ACK_ack = received[2]#not correct, ask the sender to resend the packet
        TCPsocket.send(str(ACK_sequence) + ',' + str(ACK_ack))
        logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), UDP_HOST , sender_IP, 0,ACK_ack , ackflag, finflag, 'Succeed') 
    
    while True:
        UDPrecdata = UDPsocket.recvfrom(576*5) #receive the data 
       
        length_seg = len(UDPrecdata[0]) - 20
        received = struct.unpack('!HHIIHHHH%ds'%length_seg, UDPrecdata[0]) #unpack the data
        sum_output = varify_check(UDPrecdata[0])# validate the checksum
        if received[4] == 0:
            ackflag = 0
            finflag = 0
        elif received[4] == 1:
            ackflag = 0
            finflag = 1
        elif received[4] == 16:
            ackflag = 1
            finflag = 0
        elif received[4] == 17: #receive the fin flag to close the UDP connect
            ackflag = 1
            finflag = 1
            ACK_sequence = received[3]
            ACK_ack = received[2] + len(received[8]) #write to the log file
            logwriting(((int(received[2])+576) / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), sender_IP, UDP_HOST, received[2], received[3], ackflag, finflag, 'Received')
            logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), UDP_HOST , sender_IP, ACK_sequence,ACK_ack , ackflag, finflag, 'Succeed')
            TCPsocket.send(str(ACK_sequence) + ',' + str(ACK_ack)) #send an ack to sender then sender will close the socket
            break
        if sum_output == 65535: #the packet is uncorrupted, write the situation to the logfile and the packet is received
            logwriting((int(received[2]) / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), sender_IP, UDP_HOST, received[2], received[3], ackflag, finflag, 'Received')
            print 'The packet is uncorrupted' 
            wrto_file(writefile,received)
            ACK_ack = received[2] + (len(UDPrecdata[0])-20)
            ACK_sequence = received[3]
            
            TCPsocket.send(str(ACK_sequence) + ',' + str(ACK_ack))
            logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), UDP_HOST , sender_IP, ACK_sequence,ACK_ack , ackflag, finflag, 'Succeed') 
        else:
            print 'The packet is corrupted' #the packet is corrupted, write the situation to the log file and the packet will be dropped.
            logwriting((int(received[2]) /(Max_segement*window_size)+ 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), sender_IP, UDP_HOST, received[2], received[3], ackflag, finflag, 'Dropped')
            ACK_ack = received[2]
            ACK_sequence = received[3]
            TCPsocket.send(str(ACK_sequence) + ',' + str(ACK_ack))
            logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), UDP_HOST , sender_IP, ACK_sequence,ACK_ack , ackflag, finflag, 'Succeed')
            
        
    
    print 'Delivery completed successfully'
        
               
    
    
    
    
    