# This is completed by Sihan Wu, Yihan Dai, Yitong Wang together
import web

import MySQLdb
import smbus
import time     # import kinds of library we need



con = MySQLdb.connect(host='cloudgroup7.cloudapp.net',user='shuai',passwd='123456',db='iot') 


bus = smbus.SMBus(1)
Device_Address = 0x41
bus.write_byte(Device_Address,0x02)
bus.write_byte(Device_Address,0x00)
bus.write_byte(Device_Address,0x00)    #configure the sensor

def get():

	now = str(datetime.now())         # make string "now" store present time

	bus.write_byte(Device_Address, 0x00) # request device to read temperature
	time.sleep(0.015)
	tem=bus.read_byte(Device_Address)
	tem=(tem/float(256))*165-40			# transform temperature into appropriate format
	print tem							#  output temperature
	bus.write_byte(Device_Address, 0x01) #request device to read humidity
	time.sleep(0.015)					 # wait 0.015 second
	hum=bus.read_byte(Device_Address)
	hum=(hum/float(256))*100			 # also transform number
	print hum
	cur=con.cursor()

	
	cur.execute('insert into info (temp, humi) values (%s,%s)' ,(tem,hum))
        con.commit()
	# insert temperature and humidity into info table


	cur.execute('select * from info')   #read info table
	rows = cur.fetchall()
	for eachRow in rows:		# read every row and print		
		print eachRow


	cur.close()
	con.commit()


if __name__ == "__main__": 

	

	j=0

	while 1 == 1:            # this part makes sensor read temp and hum every 5 seconds
		get()
		time.sleep(5)
		j +=1
		print j
	
	con.close
    

