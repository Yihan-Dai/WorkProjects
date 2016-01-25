# this code is completed by Sihan Wu, Yihan Dai and Yitong Wang together
import meArm
import time
import smbus
import lab1_1
import Adafruit_CharLCD as LCD

lcd = LCD.Adafruit_CharLCDPlate()


arm = meArm.meArm()
arm.begin() 
x=0
y=100
z=50

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

  
    
def move_forward():            # define every function
    global y
    y=y+50                     # only make the value of y changes
    if -219<=y and y<=219:     # detect the range of y
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
        lcd.message('wrong')   # if instructions will make arm go beyond range, then show"wrong"
        time.sleep(3.0)
    
def move_backward():
    global y
    y=y-50
    if -219<=y and y<=219:
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')   # if instructions will make arm go beyond range, then show"wrong"
        time.sleep(3.0)
    
def move_up():
    global z
    z=z+50                     # only make the value of z changes
    if -156<=z and z<=156:
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')   # if instructions will make arm go beyond range, then show "wrong"
        time.sleep(3.0)
def move_down():               # then we deine every function, respectively
    global z
    z=z-50
    if -156<=z and z<=156:
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)
    
def turn_left():
    global x
    x=x-50
    if -195<=x and x<=195:
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)
    
def turn_right():
    global x
    x=x+50
    if -195<=x and x<=195:
    	arm.gotoPoint(x,y,z)
    else:
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)
    
def open_gripper():
    arm.openGripper()
    
def close_gripper():
    arm.closeGripper()

def show_temperature():         # define a function called show_temperature
    lcd.set_color(1.0, 0.0, 0.0)
    lcd.clear()
    lcd.message('%.4f C'%tem)
    time.sleep(3.0)

def show_humidity():            # define a function called show_humidity
    lcd.set_color(1.0, 1.0, 0.0)
    lcd.clear()
    lcd.message('%.4f %%'%hum)
    time.sleep(3.0)

button=[LCD.SELECT, 'Recording Start', (1,1,1)]


while True:                    # provide repeating recording function
    lcd.message('Press Select button...')  # ask user to press select button
    
    if  lcd.is_pressed(button[0]):          
        lcd.clear()
        lcd.message(button[1])            # ask user to record voice
        lcd.set_color(button[2][0], button[2][1], button[2][2])
        
        stuff="sh /home/pi/mystuff/lab3/voice.sh"#transform voice to txt    
        lab1_1.recording(stuff)
        flac="/home/pi/mystuff/lab3/voice.flac"
        message=lab1_1.stt_google(flac)   # return the txt
        
        
        if message=="show temperature":   # recognize the txt
            show_temperature()            
        elif message=="show humidity":
            show_humidity()
        elif message=="move forward":     # recognize the instructions
            move_forward()  
        elif message=="move backward":
            move_backward()
        elif message=="move up":
            move_up()
        elif message=="move down":
            move_down()
        elif message=="turn left":
            turn_left()
        elif message=="turn right":
            turn_right()
        elif message=="open gripper":
            open_gripper()
        elif message=="close gripper":
            close_gripper()
        else:                     # if user doesn't give right instructions, then screen will display"wrong"
            lcd.clear()
            lcd.message('wrong')
            time.sleep(3.0)

        
 

