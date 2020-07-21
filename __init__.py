from flask import Flask, request, url_for, render_template
import datetime
import os
import mysql.connector
app = Flask(__name__)


path2 = 'static/date.csv'

mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='ss861008',
    database='memo'
)

@app.route('/', methods=['GET','POST'])
def index():
        if request.method == 'POST':
                mycursor = mydb.cursor()
                message = request.form["memo"]
                insert_stmt = ("select exists ( select * from sentence where id = 1)")
                insert_stmt2 = ("insert into sentence (poem)" "values (%s)")
                insert_stmt3 = ("update sentence set poem = %s where id = 1")
                mycursor.execute(insert_stmt)
                content = mycursor.fetchone()
                if content == None:
                        mycursor.execute(insert_stmt2,(message,))
                else:
                        mycursor.execute(insert_stmt3,(message,))
                mydb.commit()
                select_stmt = "SELECT poem FROM sentence WHERE poem = %(poem)s"                
                mycursor.execute(select_stmt, { 'poem': message })
                myresult = mycursor.fetchone()
                message = str(myresult[0])
                mycursor.execute('SELECT updatetime FROM sentence where id = 1')
                myresult2 = mycursor.fetchone()
                updatetime = str(myresult2[0])
                return render_template('index.html', message=message, update_date=updatetime)
        else:
                mycursor = mydb.cursor()
                mycursor.execute('SELECT poem FROM sentence where id = 1')
                myresult = mycursor.fetchone()
                message = str(myresult[0])
                mycursor.execute('SELECT updatetime FROM sentence where id = 1')
                myresult2 = mycursor.fetchone()
                updatetime = str(myresult2[0])
                return render_template('index.html', message=message, update_date=updatetime)



if __name__ == "__main__":
    app.run()