__author__ = 'illuminati'
import mysql.connector
import mysql.connector.cursor
from flask import request
from flask import Flask
from werkzeug.contrib.fixers import LighttpdCGIRootFix
app = Flask(__name__)
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
cnx = mysql.connector.connect(user='root', password = 'pilock', host='127.0.0.1', database = 'pilock')
global currentlyLocked
currentlyLocked = [False,]


@app.route('/open', methods=['POST'])
def open():
    querry = ("select * from users where name = %s ")
    try:
        cursor = cnx.cursor()
        cursor.execute(querry, (request.form['username'],))
        result = cursor.fetchall()
        if len(result)  > 0:
            if currentlyLocked[0] == True:
                currentlyLocked[0] = False
                return 'open'
            else:
                return "Aleady Open"
        else:
           return 'denied'
        cursor.close()
    except Exception, err:
        print Exception,err

@app.route('/lock',methods=['POST'])
def lock():
    querry = ("select * from users where name = %s ")
    try:
        cursor=cnx.cursor()
        cursor.execute(querry, (request.form['username'],))
        result = cursor.fetchall()
        if len(result)  > 0:
            if currentlyLocked[0] == True:

                return "Already Locked"

            else:
                currentlyLocked[0] = True
                return "locked"
        else:
           return 'denied'
        cursor.close
    except Exception, err:
        print Exception,err
@app.route('/adduser',methods=['POST'])
def adduser():
    try:
        insert = (request.form['username'],request.form['type'])
        cursor = cnx.cursor()
        querry = ("insert into users (name, type) VALUES (%s,%s)")
        cursor.execute(querry, insert)
        result = cursor.fetchall
        print(cursor.statement + " " + str(cursor.rowcount))
        cursor.close
        cnx.commit()
        return "successful"
    except Exception, err:
        print Exception,err

if __name__ == '__main__':
    app.run()
