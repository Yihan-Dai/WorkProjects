#this lab is completed by Sihan Wu, Yihan Dai and Yitong Wang together
import web
import meArm
import Adafruit_CharLCD as LCD
lcd = LCD.Adafruit_CharLCDPlate()
import time                          # import several libraries we need
urls = {
    '/robot', 'robot'                # set up url address
}

arm = meArm.meArm()
arm.begin() 
arm.closeGripper()
x=0
y=100
z=50


def move_forward():            #define every function
    global y
    y=y+50                     # only make the value of y changes
    if -219<=y and y<=219:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('Move forward')
    else:
        y=y-50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
        lcd.message('wrong')       # if instructions will make arm go beyond range, then display wrong
        time.sleep(3.0)
    
def move_backward():
    global y
    y=y-50
    if -219<=y and y<=219:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('Move backward')
    else:
        y=y+50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
        lcd.message('wrong')
        time.sleep(3.0)
    
def move_up():
    global z
    z=z+50                  # only make the value of z changes
    if -156<=z and z<=156:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
        lcd.message('Move up')     # make LCD display the instructions
    else:
        z=z-50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)

def move_down():
    global z
    z=z-50
    if -156<=z and z<=156:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('Move down')
    else:
        z=z+50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)
    
def move_left():
    global x
    x=x-50                          # only make the value of x changes
    if -195<=x and x<=195:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('Move left')
    else:
        x=x+50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
        lcd.message('wrong')        # if go beyond range, then show wrong
        time.sleep(3.0)
    
def move_right():
    global x
    x=x+50
    if -195<=x and x<=195:
    	arm.gotoPoint(x,y,z)
        lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('Move right')
    else:
        x=x-50
    	lcd.set_color(1.0, 0.0, 0.0)
    	lcd.clear()
    	lcd.message('wrong')
        time.sleep(3.0)

class robot:                        # define robot class
    def GET(self):
	return data
    def POST(self):
	global data
    data = web.data()               # receive the instruction from ios app
	print data
	
    if data == "move forward":      # judge the instructions from app and execute instructions
	    move_forward()
	elif data == "move backward":
	    move_backward()
	elif data == "move up":
	    move_up()
	elif data == "move down":
	    move_down()
	elif data == "move left":
	    move_left()
	elif data == "move right":
	    move_right()
	elif data=="open":
     	    arm.openGripper()
	elif data=="close":
	    arm.closeGripper()
	elif data =="reset":
            arm.begin() 
else:                              #  if the instruction is not right then LCD display wrong
	    lcd.clear()
        lcd.message('Wrong')
        time.sleep(3.0)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
	

