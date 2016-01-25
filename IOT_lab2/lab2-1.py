# This part is mainly completed by Yitong Wang
import smbus
import time
bus=smbus.SMBus(1)
Device_Address=0x41                    
bus.write_byte(Device_Address,0x02)
bus.write_byte(Device_Address,0x00)
bus.write_byte(Device_Address,0x00)
# these steps only config the sensor

#temperature output
bus.write_byte(Device_Address,0x00)    #request the device to read the temperature 
time.sleep(0.015)                      #wait 0.015s
tem=bus.read_byte(Device_Address)
tem=(tem/float(256))*165-40
print "Temperature %.4f C"%tem         #print temperature(4 digits after the decimal point) 

#Humidity Output
bus.write_byte(Device_Address,0x01)    #request the device to read the humidity 
time.sleep(0.015)                      #wait 0.015s
hum=bus.read_byte(Device_Address)      
hum=(hum/float(256))*100
print "Humidity %.4f %%" %hum          #print humidity(4 digits after the decimal point) 


