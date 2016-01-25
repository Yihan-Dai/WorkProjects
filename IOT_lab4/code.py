#This lab is accomplished by Yihan Dai, Yitong Wang and Sihan Wu together.
import web    #import some useful libraries
import MySQLdb
render = web.template.render('templates/')   #detect the .html files from templates dictory.
db = web.database(dbn='mysql', user='root', pw='123321', db='iot') #visit the database 'iot'

from web import form   

urls = (                 #one-to-one mapping: URL - class
    '/main', 'index',    #main page
    '/history','history', #history records
    '/sensor/temperature','show_temperature',
    '/sensor/humidity','show_humidity',
    '/add', 'add', 
    '/delete','clear',  #clear the history records
    '/mail','mail',     #send the email
    '/mail1','mail1',
    '/history1','history1',
    '/','login'         #login interface
)

myform=form.Form(       #define a form named myform with some arguments for sending emails
    form.Textbox("Receiver"),
    form.Textbox("Subject"),
    form.Textarea('Message'))

myform2=form.Form(      #define a form called myform2 for users login
    form.Textbox("Username"),
    form.Textbox("Password"))

class login:            #define a class called login
    def GET(self):
        log = myform2()
        return render.mail(log) #display the form for the users
    
    def POST(self):
        log = myform2()
        if not log.validates():  #if not validated, display again
            return render.mail(log)
        else:                    #if validated, information used to check with the database
	    user_name=log.d.Username
            pwd=log.d.Password
            l = db.select('login')
            for login in l:      #if correct, redirect to the '/main'
                if login.user==user_name and login.password==pwd:
                    raise web.seeother('/main')
                else:
                    continue
            raise web.seeother('/') #not correct, indicate users input the information again

            
            
class mail:    #define a class named mail
    def GET(self):
        ip_addr=web.ctx.get('ip')    #insert the ip address and method to the history database
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        f = myform()
        return render.mail(f)       #displat the mail interface for the user

    def POST(self):
        ip_addr=web.ctx.get('ip')    #if someone post some information, add the history records
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        f = myform()
        if not f.validates():  #if not validated, display the mail interface for the user again
            return render.mail(f)
        else:                  #if validated, send the email and redirect the previous page
            web.config.smtp_server = 'smtp.gmail.com' #config the stmp server
            web.config.smtp_port = 587
            web.config.smtp_username = 'iot.group8@gmail.com'
            web.config.smtp_password = 'dagezuiniubi'
            web.config.smtp_starttls = True
            web.sendmail('iot.group8@gmail.com', f.d.Receiver, f.d.Subject, f.d.Message)
            raise web.seeother('/mail')

class index:  #main page
    def GET(self):
        c = db.select('content')  #record the history
        ip_addr=web.ctx.get('ip')
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        return render.content(c)

class history: #history recordds
    def GET(self):
        ip_addr=web.ctx.get('ip')  #record the history
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        h = db.select('history')
        return render.history(h)
    
class show_temperature:  #define a class to show the temperature, just for test
    def GET(self):
        return 'TEMPERATURE =0'

class show_humidity:#define a class to show the humidity, just for test
    def GET(self):
        return 'Humidity=0'

class history1:     #this is for the history button in the main page
    def POST(self):
        ip_addr=web.ctx.get('ip')
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        raise web.seeother('/history')

class mail1:      #this is for the mail button in the main page
    def POST(self):
        ip_addr=web.ctx.get('ip')
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        raise web.seeother('/mail')

class clear:  #used to clear the history records
    def POST(self):
        d=db.delete('history', where='1=1')
        ip_addr=web.ctx.get('ip')
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        raise web.seeother('/history')
        

class add:     #add some contents in the main page and display it.
    def POST(self):
        i = web.input()
        n = db.insert('content', title=i.title)
        ip_addr=web.ctx.get('ip')
        msg=web.ctx.get('method')
        db.insert('history', ip=ip_addr,method=msg)
        raise web.seeother('/')


if __name__ == "__main__":
    app = web.application(urls, globals())  
    app.run()           #run the app


