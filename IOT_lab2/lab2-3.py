# This part(2-3) is mainly completed by Yihan Dai
# The robotics arm is completed by Sihan Wu, Yitong Wang and Yihan Dai together.
import time
import smbus
import lab1_1
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
tem=(tem/float(256))*165-40

#humidity output
bus.write_byte(Device_Address,0x01)
time.sleep(0.015)
hum=bus.read_byte(Device_Address)
hum=(hum/float(256))*100


def show_temperature():         #define a function called show_temperature
    lcd.set_color(1.0, 0.0, 0.0)
    lcd.clear()
    lcd.message('%.4f C'%tem)
    time.sleep(3.0)

def show_humidity():            #define a function called show_humidity
    lcd.set_color(1.0, 1.0, 0.0)
    lcd.clear()
    lcd.message('%.4f %%'%hum)
    time.sleep(3.0)

button=[LCD.SELECT, 'Recording Start', (1,1,1)]


while True:                    #provide repeating recording function
    lcd.message('Press Select button...')  #ask user to press select button
    
    if lcd.is_pressed(button[0]):          
	lcd.clear()
	lcd.message(button[1])             #ask user to record voice
	lcd.set_color(button[2][0], button[2][1], button[2][2])
        
        stuff="sh /home/pi/mystuff/voice.sh"#transform voice to txt    
        lab1_1.recording(stuff)
        flac="/home/pi/mystuff/voice.flac"
        message=lab1_1.stt_google(flac)   #return the txt
        
        
        if message=="show temperature":   #recognize the txt
            show_temperature()            
        elif message=="show humidity":
            show_humidity()
        else:
            lcd.clear()
            lcd.message('%r'%message)
            time.sleep(3.0)

        
 

