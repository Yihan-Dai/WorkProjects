================================================================
This is a Simple TCP-like transport layer protocol written in Python 2.7.3.

Written by Yihan Dai
Nov,9 2015

================================================================
This programming assignment consists of three parts:

    sender.py
    receiver.py
    sender_file.txt

(a) Requirement of this coursework:
    This assignment require to implement a simplified TCP-­like transport layer protocol. The protocol should provide reliable, in order delivery of a stream of bytes. It should   
    recover from in­-network packet loss, packet corruption, packet duplication and packet reordering and should be able cope with dynamic network delays. Data is exchanged via a  
    link emulator to provide a unreliable transmission. The acknowledgements should be directly sent from receiver to the sender without loss.
    In my code, i use the stop-and-wait protocol to establish a TCP protocol model. Hence, the window size should be 1. That means each time only one packet is delivered. When the 
    window size chosen is larger than 1, two more or three more packets will be combined into one packet and delivered to the receiver. There will be no kind of reorder phenomenon
    due to the stop-and-wait protocol.


(b) Instructions:
1. sender.py is a sending data while receiving ack response program. It can be invoked as below in the terminal:

   python sender.py <filename> <remote_IP> <remote_port> <ack_port_num> <log_filename> 
   <window_size> 
   
   It consists of three main parts. Firstly, the program reads all the data from the original file and into a list[]. With each element in the list[], a header includes Destination 
   port, Source port, Sequence number, Ack number, Ack flag, Fin Flag, window size and checksum will be packed and delivered to receiver. Then, the program can choose send the next    
   packet or resend the previous packet due to the different Ack responses. In the last, it will set the Fin flag as 1 and deliver a segment to receiver. The program receiver the
   Ack response and close TCP socket.

2. receiver.py is a receiving data while sending ack response program. It can be invoked as below in the terminal:

   python receiver.py <filename> <listening_port> <sender_IP> <sender_port> <log_filename>

   The receiver program will establish a UDP socket and receive the data from sender. Secondly, it will check the correctness of each packet through verify the checksum. Finally, it   
   will unpack the data and write the application data into the file. Until Fin flag set as 1, the receiver program will close the TCP socket.

(c) Program descriptions:
1. Tcp segments structure:
   ——————————————————————————————————————————————————
   |Destination port# 2 bytes | Source port# 2 bytes|
   ——————————————————————————————————————————————————
   |         Sequence number# 4 bytes               |
   ——————————————————————————————————————————————————
   |            ACK number# 4 bytes                 |
   ——————————————————————————————————————————————————
   |ACK (1 bit) | FIN (1 bit) | 0x00xx # 2 bytes    |
   ——————————————————————————————————————————————————
   |            Window size# 2 bytes                |
   ——————————————————————————————————————————————————
   |    Checksum# 2 bytes     | Unused# 2 bytes     |
   ——————————————————————————————————————————————————
   |         Application layer data# 576 bytes      |
   |                                                |
   |                                                |
   ——————————————————————————————————————————————————

   The total length of the header is 20 bytes. Unused bits occupy in 2 bytes. ACK bit is always be 1 because the ACK response is transmitted via a TCP socket from receiver to 
   sender.

2. Functions:
2.1 sender mechanism
    Deal with corruption: The sender program will resend the packet if the response received indicates the corruption.
    Deal with Timeout/packet loss: The sender program will resend the packet if no response received until the timeout.
    Deal with reorder: The stop-and-wait protocol will ensure no reorder situation.
    Deal with the correct ACK: Send the next packet.
2.2 receiver mechanism
    Drop the corrupted packet and ask the sender program to resend it.
    Receive the uncorrupted packet and ask the sender program to send next.
    No response with the packet loss
    Deal with the duplicated packet: Ignore the already ACKed packet due to the daly in 
    the proxy.

(d) Output Sample:
1. proxy:
    $ ./newudpl -vv -i 160.39.252.174:* -o 160.39.252.174:4119 -d1.5 -B 1000 -L 20 -O 5
    ————————————————————————————————————————————————————————————————
    Network Emulator With UDP Link
    Copyright (c) 2001 by Columbia University; all rights reserved

    Link established:
    dyn-160-39-252-174.dyn.columbia.edu(160.39.252.174)/***** ->
          dyn-160-39-252-174.dyn.columbia.edu(160.39.252.174)/41192
    /41193 ->
          dyn-160-39-252-174.dyn.columbia.edu(160.39.252.174)/4119

    emulating speed  : 1000(kb/s)
    delay            : 1.700000(sec)
    ether net        : 10M(b/s)
    queue buffer size: 8192(bytes)

    error rate
        random packet loss: 20(1/100 per packet)
        bit error         : 10000(1/100000 per bit)
        out of order      : 5(1/100 per packet)

2. receiver
    $ python receiver.py write.txt 4119 160.39.252.174 4118 log_recv.txt 
    It will print all the uncorrupted packet.
    ————————————————————————————————————————————————————————————————
    The ip address is : 160.39.252.174
    Waiting for the packet

    ………………
    
    Delivery completed successfully

3. sender:
    $ python sender.py sender_file.txt 160.39.252.174 41192 4118 log_sender.txt 1 
   
------------------------------------------------------------------------------
Sending from:                                      sender_file.txt
File size:                                         8112
Sender IP:                                         160.39.252.174
Sender port:                                       4118
Sender log filename:                               log_sender.txt
Receiver IP:                                       160.39.252.174
Receiver port:                                     41192
Window size:                                       1
------------------------------------------------------------------------------
Connection established
Resend the corrupted packet
Resend the corrupted packet
Send the packet successfully
Time out resend
Time out resend
Resend the corrupted packet
Send the packet successfully
Send the packet successfully
Send the packet successfully
Resend the corrupted packet
Resend the corrupted packet
Resend the corrupted packet
Time out resend
Send the packet successfully
Resend the corrupted packet
Send the packet successfully
Send the packet successfully
Send the packet successfully
Time out resend
Resend the corrupted packet
Resend the corrupted packet
Time out resend
Time out resend
Send the packet successfully
Resend the corrupted packet
Time out resend
Resend the corrupted packet
Send the packet successfully
Resend the corrupted packet
Send the packet successfully
Send the packet successfully
Time out resend
Send the packet successfully
Resend the corrupted packet
Resend the corrupted packet
Send the packet successfully
Send Fin flag successfully
Delivery completed successfully
------------------------------------------------------------------------------
Total bytes sent:                                  16224
Total Segments sent:                               38
Segments retransmitted due to corruption:          14
Segments retransmitted due to sender timeout:      8
Total retransmitted segments:                      22
Transmission time (s):                             67.89
------------------------------------------------------------------------------

4. log_recv.txt
Segment#  Trans_direction     Timestamp             Source         Destination    Sequence#  ACK#   ACK  FIN  Trans_status
1         Sender -> Receiver  09,Nov,2015 20:01:18  160.39.252.174 160.39.252.174 0          0      1    0    Dropped 
-         Receiver -> Sender  09,Nov,2015 20:01:18  160.39.252.174 160.39.252.174 0          0      1    0    Succeed 
1         Sender -> Receiver  09,Nov,2015 20:01:19  160.39.252.174 160.39.252.174 0          1      1    0    Dropped 
-         Receiver -> Sender  09,Nov,2015 20:01:19  160.39.252.174 160.39.252.174 1          0      1    0    Succeed 
1         Sender -> Receiver  09,Nov,2015 20:01:21  160.39.252.174 160.39.252.174 0          2      1    0    Received
-         Receiver -> Sender  09,Nov,2015 20:01:21  160.39.252.174 160.39.252.174 2          576    1    0    Succeed 
2         Sender -> Receiver  09,Nov,2015 20:01:28  160.39.252.174 160.39.252.174 576        3      1    0    Dropped 
-         Receiver -> Sender  09,Nov,2015 20:01:28  160.39.252.174 160.39.252.174 3          576    1    0    Succeed 
2         Sender -> Receiver  09,Nov,2015 20:01:29  160.39.252.174 160.39.252.174 576        4      1    0    Received
-         Receiver -> Sender  09,Nov,2015 20:01:29  160.39.252.174 160.39.252.174 4          1152   1    0    Succeed 
3         Sender -> Receiver  09,Nov,2015 20:01:31  160.39.252.174 160.39.252.174 1152       5      1    0    Received
-         Receiver -> Sender  09,Nov,2015 20:01:31  160.39.252.174 160.39.252.174 5          1728   1    0    Succeed 
4         Sender -> Receiver  09,Nov,2015 20:01:33  160.39.252.174 160.39.252.174 1728       6      1    0    Received
-         Receiver -> Sender  09,Nov,2015 20:01:33  160.39.252.174 160.39.252.174 6          2304   1    0    Succeed 
5         Sender -> Receiver  09,Nov,2015 20:01:34  160.39.252.174 160.39.252.174 2304       7      1    0    Dropped 
-         Receiver -> Sender  09,Nov,2015 20:01:34  160.39.252.174 160.39.252.174 7          2304   1    0    Succeed 
5         Sender -> Receiver  09,Nov,2015 20:01:36  160.39.252.174 160.39.252.174 2304       8      1    0    Dropped 
…………………

5. log_sender.txt
Segment#  Trans_direction     Timestamp             Source         Destination    Sequence # ACK #  ACK  FIN  EstimateRTT(s) Timeout(s)     Trans_status   resend_marks
1         Sender -> Receiver  09,Nov,2015 20:01:18  160.39.252.174 160.39.252.174 0          0      1    0    1.96360737085  2.21835577488  Failed         Corrup_resend
-         Receiver -> Sender  09,Nov,2015 20:01:18  160.39.252.174 160.39.252.174 0          0      1    0    -              -              Received       -         
1         Sender -> Receiver  09,Nov,2015 20:01:19  160.39.252.174 160.39.252.174 0          1      1    0    1.93193220347  2.34471967816  Failed         Corrup_resend
-         Receiver -> Sender  09,Nov,2015 20:01:19  160.39.252.174 160.39.252.174 1          0      1    0    -              -              Received       -         
1         Sender -> Receiver  09,Nov,2015 20:01:21  160.39.252.174 160.39.252.174 0          2      1    0    1.90378781501  2.41038914025  Succeed                  
-         Receiver -> Sender  09,Nov,2015 20:01:21  160.39.252.174 160.39.252.174 2          576    1    0    -              -              Received       -         
2         Sender -> Receiver  09,Nov,2015 20:01:23  160.39.252.174 160.39.252.174 576        3      1    0    1.90378781501  2.41038914025  Timeout        Timeout_resend
2         Sender -> Receiver  09,Nov,2015 20:01:26  160.39.252.174 160.39.252.174 576        3      1    0    1.90378781501  2.41038914025  Timeout        Timeout_resend
2         Sender -> Receiver  09,Nov,2015 20:01:28  160.39.252.174 160.39.252.174 576        3      1    0    1.87909033697  2.43192367721  Failed         Corrup_resend
-         Receiver -> Sender  09,Nov,2015 20:01:28  160.39.252.174 160.39.252.174 3          576    1    0    -              -              Received       -         
2         Sender -> Receiver  09,Nov,2015 20:01:29  160.39.252.174 160.39.252.174 576        4      1    0    1.85793616822  2.42064035463  Succeed                  
-         Receiver -> Sender  09,Nov,2015 20:01:29  160.39.252.174 160.39.252.174 4          1152   1    0    -              -              Received       -         
3         Sender -> Receiver  09,Nov,2015 20:01:31  160.39.252.174 160.39.252.174 1152       5      1    0    1.83945350989  2.390860258    Succeed                  
-         Receiver -> Sender  09,Nov,2015 20:01:31  160.39.252.174 160.39.252.174 5          1728   1    0    -              -              Received       -         
4         Sender -> Receiver  09,Nov,2015 20:01:33  160.39.252.174 160.39.252.174 1728       6      1    0    1.82282994689  2.35274994899  Succeed                  
-         Receiver -> Sender  09,Nov,2015 20:01:33  160.39.252.174 160.39.252.174 6          2304   1    0    -              -              Received       -         
5         Sender -> Receiver  09,Nov,2015 20:01:34  160.39.252.174 160.39.252.174 2304       7      1    0    1.80880133995  2.30444159009  Failed         Corrup_resend
-         Receiver -> Sender  09,Nov,2015 20:01:34  160.39.252.174 160.39.252.174 7          2304   1    0    -              -              Received       -         
5         Sender -> Receiver  09,Nov,2015 20:01:36  160.39.252.174 160.39.252.174 2304       8      1    0    1.79626530014  2.25574776642  Failed         Corrup_resend
……………