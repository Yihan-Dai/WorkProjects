'''
The file is created by Yihan Dai on Nov 9, 2015.
The operating system is OSx and python 2.7.10 is used.
'''

import socket,time
import sys
import os
from time import strftime

Max_segement = 576 # MSS the maximum segement
file_list = []     #define a list including all the packets
Ack_num = 0        #ack number from sender to receiver 
Sequen_num = 0     #sequence number from sender to receiver
total_segement = 0  #total segments sent
corr_segement = 0   #segments due to corruption
TimeOutSegement = 0  #segments due to timeout
total_bytes = 0      # the total bytes sent
file_size = 0        #file size
import struct


def read_file(filename):  #read file into the file_list
    datafile = os.stat(filename)
    fileopen = open(filename,"r")
    for num in range(datafile.st_size / (Max_segement*window_size)):
        packet=fileopen.read(Max_segement*window_size)
        file_list.append(packet)
    packet=fileopen.read(datafile.st_size % (Max_segement*window_size))
    file_list.append(packet)
    fileopen.close()
    return datafile.st_size #return the file size
    
def header(dest_port, source_port, seq_num, ack_num, ACK_flag, FIN_flag, checksum, packet,window_size):
    if ACK_flag == 0 and FIN_flag == 0:  #pack the header with the application data
        flag = 0         #0x0000
    elif ACK_flag == 0 and FIN_flag == 1:
        flag = 1         #0x0001
    elif ACK_flag == 1 and FIN_flag == 0:
        flag = 16        #0x0010
    elif ACK_flag == 1 and FIN_flag == 1:
        flag = 17        #0x0011
        
    header = struct.pack('!HHIIHHHH%ds'%len(packet), dest_port, source_port, seq_num, ack_num, flag, window_size, checksum, 0, packet)
    
    return header

def cal_checksum(header_str):      #calculate the checksum 
    
    sum_calc = 0
    

    #Divide the string by 16 bits and calculate the sum
    for num in range(len(header_str)):
        if num % 2 == 0:     # Even parts with higher order
            sum_calc = sum_calc + (ord(header_str[num]) << 8)
        elif num % 2 == 1:   # Odd parts with lower order
            sum_calc = sum_calc + ord(header_str[num])
    
    # Get the inverse as the checksum
    checksum = 65535 - (sum_calc % 65536)                       
    
    return checksum



def logwriting(segment_num, direction, timestamp, source, destination, sequence_num, ACK_num, ackflag, finflag, estimateRTT, timeout, trans_status, notes):
    #write to log file
    
    #Determine the writing direction    
    if direction == 'forward':
        logdirection = 'Sender -> Receiver'
    elif direction == 'backward':
        logdirection = 'Receiver -> Sender'
    else:
        logdirection = direction
    
    #Log line format    
    logline = str(segment_num).ljust(10) + logdirection.ljust(20) + timestamp.ljust(22) + source.ljust(15) + destination.ljust(15) + str(sequence_num).ljust(11) + \
              str(ACK_num).ljust(7) + str(ackflag).ljust(5) + str(finflag).ljust(5) + str(estimateRTT).ljust(15) + str(timeout).ljust(15) + trans_status.ljust(15) + str(notes).ljust(10) + '\r\n'    
    
    #Check the output method (stdout or write to a log file)
    if log_filename == 'stdout.txt':
        print logline
    else:
        try:
            logfile = open (log_filename, "a")
        except:
            print 'Unable to open file'
        logfile.write(logline)
        logfile.close()
    
    return

def recv_ack(conn,remote_port, ack_port_num, Sequen_num, Ack_num,TimeoutInterval,t_start):
    global total_segement, corr_segement, TimeOutSegement, total_bytes
    alpha = 0.125
    beta = 0.25
    SampleRTT = 1
    EstimatedRTT = 2
    packet_num=1
    DevRTT = 0
    while True:
        
        conn.settimeout(TimeoutInterval)
        try:
            ack = conn.recv(1024)

            
        
            t_stop = time.time() #stop the timer
            SampleRTT = t_stop - t_start #calculate the timeout interval
            EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT
            DevRTT = (1 - beta) * DevRTT + beta * abs(SampleRTT - EstimatedRTT)
            TimeoutInterval = EstimatedRTT + 4 * DevRTT    
            
        
            # Fin flag, close the socket 
            if packet_num == total_packet and int(ack[ack.find(',')+1:]) == (Sequen_num+len(file_list[packet_num-1])):
                trans_status = 'Succeed'
                notes = ''    #write to the log file
                logwriting((Sequen_num / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, 1, 0, EstimatedRTT, TimeoutInterval, trans_status, notes)
                logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()),remote_ip, TCP_HOST, ack[0:ack.find(',')], ack[ack.find(',')+1:], 1, 0, '-', '-', 'Received', '-') 
                Sequen_num = int(ack[ack.find(',')+1:])
                Ack_num +=1
                header_str1 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, 0, file_list[packet_num-1],window_size)
                checksum = cal_checksum(header_str1)
                header_str2 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 1, checksum, file_list[packet_num-1],window_size)
                UDPsocket.sendto(header_str2,(remote_ip,remote_port)) #send the fin flag
                t_start = time.time() #restart the timer
                
                total_segement +=1 
                total_bytes += len(file_list[packet_num-1])
                while True:
                    try:
                        ack = conn.recv(1024)  #receive the response for the fin flag and close the TCP socket
                        t_stop = time.time() #stop the timer
                        SampleRTT = t_stop - t_start #calculate the timeout interval
                        EstimatedRTT = (1 - alpha) * EstimatedRTT + alpha * SampleRTT
                        DevRTT = (1 - beta) * DevRTT + beta * abs(SampleRTT - EstimatedRTT)
                        TimeoutInterval = EstimatedRTT + 4 * DevRTT 
                        trans_status = 'Succeed'
                        notes = 'Fin Flag send'
                        print 'Send Fin flag successfully'
                        logwriting(((Sequen_num+576) / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, str(1), str(1), EstimatedRTT, TimeoutInterval, trans_status, notes)
                        logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()),remote_ip, TCP_HOST, ack[0:ack.find(',')], ack[ack.find(',')+1:], 1, 0, '-', '-', 'Received', '-')
                        break
                    except socket.timeout: #timeout, resend the fin flag
                        print 'Time out. Resend the fin flag'
                        trans_status = 'Time out'
                        notes = 'Fin flag send failed'
                        logwriting(((Sequen_num+576) / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, str(1), str(1), EstimatedRTT, TimeoutInterval, trans_status, notes)
                        UDPsocket.sendto(header_str2,(remote_ip,remote_port))
                        t_start = time.time() #restart the timer
                        total_segement +=1
                        TimeOutSegement +=1
                        total_bytes += len(file_list[packet_num-1])
                break
            if int(ack[ack.find(',')+1:]) == (Sequen_num+len(file_list[packet_num-1])):#the packet is uncorrupted
                print 'Send the packet successfully'
                trans_status = 'Succeed'
                notes = ''
                #write to the log file
                logwriting((Sequen_num / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, 1, 0, EstimatedRTT, TimeoutInterval, trans_status, notes)
                logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()),remote_ip, TCP_HOST, ack[0:ack.find(',')], ack[ack.find(',')+1:], 1, 0, '-', '-', 'Received', '-') 
                Ack_num +=1 #update the ack number
                Sequen_num += len(file_list[packet_num-1]) #update the sequence number
                header_str1 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, 0, file_list[packet_num],window_size)
                checksum = cal_checksum(header_str1)
                header_str2 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, checksum, file_list[packet_num],window_size)
                UDPsocket.sendto(header_str2,(remote_ip,remote_port))#send the next packet
                total_segement +=1
                total_bytes += len(file_list[packet_num])
                t_start=time.time() #restart the timer
                packet_num+=1
            else:  #the packet is corrupted
                
                trans_status = 'Failed'
                notes = 'Corrup_resend'
                print 'Resend the corrupted packet'
                logwriting((Sequen_num / (Max_segement*window_size)+ 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, 1, 0, EstimatedRTT, TimeoutInterval, trans_status, notes)
                logwriting('-', 'backward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()),remote_ip, TCP_HOST, ack[0:ack.find(',')], ack[ack.find(',')+1:], 1, 0, '-', '-', 'Received', '-') 
                Ack_num +=1 #update the ack number
                header_str1 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, 0, file_list[packet_num-1],window_size)
                checksum = cal_checksum(header_str1)
                header_str2 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, checksum, file_list[packet_num-1],window_size)
                UDPsocket.sendto(header_str2,(remote_ip,remote_port)) #resend the packet
                total_segement +=1
                corr_segement +=1
                total_bytes += len(file_list[packet_num-1])
                t_start=time.time() #restart the timer

            
        except socket.timeout: #time out
            print 'Time out resend'
            
            trans_status = 'Timeout'
            notes = 'Timeout_resend'
            logwriting((Sequen_num / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, 1, 0, EstimatedRTT, TimeoutInterval, trans_status, notes)
            header_str1 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, 0, file_list[packet_num-1],window_size)
            checksum = cal_checksum(header_str1)
            header_str2 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, checksum, file_list[packet_num-1],window_size)
            UDPsocket.sendto(header_str2,(remote_ip,remote_port)) #resend the packet
            total_segement +=1
            TimeOutSegement +=1
            t_start=time.time() #restart the timer

if __name__ =='__main__':
    #Invoke the program to import <filename>, <remote_IP>, <remote_port>, <ack_port_num>, <log_filename> and <window_size>
    filename = sys.argv[1]
    remote_ip = sys.argv[2]
    remote_port = int(sys.argv[3])
    ack_port_num = int(sys.argv[4])
    log_filename = sys.argv[5]
    window_size = int(sys.argv[6])
    
    file_size = read_file(filename) #read the filename
    total_packet = len(file_list)  #calculate the total packets of the file
    UDPsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#connect to the receiver via a UDP socket
    UDP_HOST = remote_ip
    Udp_port = remote_port
    
    TCPsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #establish a TCP connect for ack response
    TCP_HOST = socket.gethostbyname(socket.gethostname())
    TCP_PORT = ack_port_num
    TCPsocket.bind((TCP_HOST, TCP_PORT))
    TCPsocket.listen(10)
    print '-' * 78        #print the transmission information 
    print 'Sending from:'.ljust(50),filename
    print 'File size:'.ljust(50), file_size
    print 'Sender IP:'.ljust(50), socket.gethostbyname(socket.gethostname())
    print 'Sender port:'.ljust(50),ack_port_num
    print 'Sender log filename:'.ljust(50), log_filename
    print 'Receiver IP:'.ljust(50), remote_ip
    print 'Receiver port:'.ljust(50),remote_port
    print 'Window size:'.ljust(50), window_size
    print '-' * 78
    time.sleep(1.0)
    logwriting('Segment#','Trans_direction', 'Timestamp', 'Source', 'Destination', 'Sequence #', 'ACK #', 'ACK', 'FIN', 'EstimateRTT(s)', 'Timeout(s)', 'Trans_status', 'resend_marks')
    
    header_str1 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, 0, file_list[0],window_size)
    checksum = cal_checksum(header_str1)
    header_str2 = header(remote_port, ack_port_num, Sequen_num, Ack_num, 1, 0, checksum, file_list[0],window_size)
    UDPsocket.sendto(header_str2,(remote_ip,remote_port)) #deliver the first segment
    total_segement +=1
    total_bytes += len(file_list[0])
    t_start=time.time()
    START_TIME = time.time() #start the timer
    
    TimeoutInterval = 2
    EstimatedRTT = 2
    TCPsocket.settimeout(TimeoutInterval)
    
    Connect_socket = 1
    while Connect_socket ==1:
        try:
            conn, addr = TCPsocket.accept() #listen to the connection from any clients
            print 'Connection established'
            recv_ack(conn,remote_port, ack_port_num, Sequen_num, Ack_num,TimeoutInterval,t_start)
            Connect_socket =0    
        except socket.timeout:   #if no client connect, then resend the first segment
            trans_status = 'Timeout'
            notes = 'Timeout_resend'
            print 'Time out resend'
            logwriting((Sequen_num / (Max_segement*window_size) + 1), 'forward', strftime("%d,%b,%Y %H:%M:%S", time.localtime()), TCP_HOST, remote_ip, Sequen_num, Ack_num, 1,0, EstimatedRTT, TimeoutInterval, trans_status, notes)
            UDPsocket.sendto(header_str2,(remote_ip,remote_port))
            total_segement +=1
            TimeOutSegement +=1
            total_bytes += len(file_list[0])
            t_start=time.time()
    STOP_TIME = time.time()          #print the completed information
    print 'Delivery completed successfully'
    print '-' * 78
    print 'Total bytes sent:'.ljust(50), total_bytes
    print 'Total Segments sent:'.ljust(50), total_segement
    print 'Segments retransmitted due to corruption:'.ljust(50), corr_segement
    print 'Segments retransmitted due to sender timeout:'.ljust(50), TimeOutSegement
    print 'Total retransmitted segments:'.ljust(50), corr_segement+TimeOutSegement
    print 'Transmission time (s):'.ljust(50), round((STOP_TIME - START_TIME), 2)
    
    print '-' * 78 

        
    
        
    
    
    