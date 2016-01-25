# This part is mainly completed by Sihan Wu
import time
import smbus
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()

bus=smbus.SMBus(1)
Device_Address=0x41
bus.write_byte(Device_Address,0x02)
bus.write_byte(Device_Address,0x00)
bus.write_byte(Device_Address,0x00)
# these steps only config the sensor

#temperature output
bus.write_byte(Device_Address,0x00)
time.sleep(0.015)
tem=bus.read_byte(Device_Address)
tem=(tem/float(256))*165-40      #transform the temperature

#humidity output
bus.write_byte(Device_Address,0x01)
time.sleep(0.015)
hum=bus.read_byte(Device_Address)
hum=(hum/float(256))*100         #transform the humidity


lcd.set_color(1.0, 0.0, 0.0)     #set the color
lcd.clear()                      #clear the message 
lcd.message('%.4f C'%tem)        #print thg temperature on the lcd screen
time.sleep(3.0)                  #wait 3 seconds

lcd.clear()                   
lcd.message('%.4f %%'%hum)       #print the humidity on the lcd screen
time.sleep(3.0) 
