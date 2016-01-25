import web #import web and MySQLdb
import MySQLdb
db = web.database(dbn='mysql', user='root', pw='123321', db='iot') #connect the database 
render = web.template.render('templates/')
list=[]
urls = (              
	'/', 'index'
)

class index:
    def GET(self): #select the database, store the values 
        info = db.select('info',what='id,temp,humi',order='id DESC',limit=15)   
        return render.chart(info) #return to the chart.html

    
if __name__ == "__main__":
    app = web.application(urls, globals())  
    app.run()           