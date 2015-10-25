__author__ = 'illuminati'
import mysql.connector
import mysql.connector.cursor
from flask import request
from flask import Flask
from datetime import datetime
from werkzeug.contrib.fixers import LighttpdCGIRootFix

from local import settings
app = Flask(__name__)
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
cnx = mysql.connector.connect(user=settings.user, password = settings.passwd, host='127.0.0.1', database = 'pilock')
global currentlyLocked
currentlyLocked = [False,]

def logDbAction(userid,logAction,logTime):
    cursor = cnx.cursor()
    insert = (userid,logAction,logTime)
    querry = ("insert into logs (userid, action, time) VALUES (%s,%s, %s)")
    cursor.execute(querry, insert)
    result = cursor.fetchall
    print(cursor.statement + " " + str(cursor.rowcount))
    cursor.close
    cnx.commit()

@app.route('/open', methods=['POST'])
def open():
    querry = ("select * from users where name = %s ")
    try:
        cursor = cnx.cursor()
        cursor.execute(querry, (request.form['username'],))
        result = cursor.fetchall()
        logTime = datetime.now()
        logUserId = result[0][0]
        cursor.close()
        if len(result)  > 0:
            if currentlyLocked[0] == True:
                currentlyLocked[0] = False
                logAction = "Opened the lock"
                logDbAction(logUserId,logAction,logTime)
                return 'opend'
            else:
                logAction = "Tried to open already open lock"
                logDbAction(logUserId,logAction,logTime)
                return "Aleady Open"
        else:
           logAction = "tried to open the lock but denied due to invalid credentials"
           logDbAction(logUserId,logAction,logTime)
           return 'denied'

    except Exception, err:
        print Exception,err

@app.route('/lock',methods=['POST'])
def lock():
    querry = ("select * from users where name = %s ")
    try:
        cursor=cnx.cursor()
        cursor.execute(querry, (request.form['username'],))
        result = cursor.fetchall()
        logTime = datetime.now()
        logUserId = result[0][0]
        cursor.close()
        if len(result)  > 0:
            if currentlyLocked[0] == True:
                logAction = "Attempted to lock already locked lock"
                logDbAction(logUserId,logAction,logTime)
                return "Already Locked"

            else:
                logAction = "Locked the lock"
                logDbAction(logUserId,logAction,logTime)
                currentlyLocked[0] = True
                return "locked"
        else:
           logAction = "tried to lock the lock but denied due to invalid credentials"
           logDbAction(logUserId,logAction,logTime)
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
        
        logTime = datetime.now()
        logUserId = cursor.lastrowid
        
        cursor.close()
        cnx.commit()
        logAction = "User " + insert[0] + " added with type " + insert[1]
        logDbAction(logUserId,logAction,logTime)
        return "successful"
    except Exception, err:
        print Exception,err

if __name__ == '__main__':
    app.run()
