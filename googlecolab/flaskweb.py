# -*- coding: utf-8 -*-



!pip install flask-ngrok
!pip install flask-bootstrap

from flask_ngrok import run_with_ngrok
from flask import Flask, render_template , request 
import os
from google.colab import drive
from markupsafe import escape
import sqlite3
#from flask_cores import CORS

#Mount the driver
drive.mount('/content/gdrive')

#This is to find the url for flask server host in google colab in case ngrock as login 5000 is the flask port
from google.colab.output import eval_js
print(eval_js("google.colab.kernel.proxyPort(5000)"))

app = Flask(__name__, template_folder='/content/gdrive/MyDrive/static')
#CORS(app)
run_with_ngrok(app)

def setupDb():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully");

    conn.execute('''
CREATE TABLE IF NOT EXISTS team(team text);''')

    conn.commit()

    print("Table created successfully");

    conn.close()

def insert(item):
  print(f'to insert {item}')
  conn = sqlite3.connect('test.db')
  conn.execute(f"INSERT INTO team VALUES('{item}');")
  conn.commit()
  print("data inserted successfully");
  conn.close()

def getData():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM team''')
  result=''
  for row in cursor:
    #print(row)
    result = result +"<br>" +row[0]
  
  conn.close()
  return result


def getDataArray():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM team''')
  data = cursor.fetchall()
  conn.close()
  return data

@app.route('/')
def hello():
  return 'hello world!'


@app.route('/hi/<name>')
def greeting(name):
  return f'Greetings! {name} '


@app.route('/add/<name>')
def add(name):
  insert(name)
  return f'inserted {escape(name)}!'

@app.route('/list')
def lst():
  data=getData()
  return data


@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/adddisplay', methods=['GET','POST'])
def adddisplay():
    if request.method=='GET':
      pass
    if request.method=='POST':
      item = request.form.get('item')
      insert(item)
      print(item)
    data = getDataArray()  
    return render_template('adddisplay.html', items = data)


@app.route('/mp', methods=['GET', 'POST'])
def map():
    if request.method=='GET':
      pass
    if request.method=='POST':
      item=request.form.get('item')
      insert(item)
    items=getDataArray()
    return render_template('data.html', items=items)

if __name__ == '__main__':
   setupDb()
   app.run()



"""#Home Work
Please add a new column price to the table, and change the web function to add new field price on the web,
so when the web submit is clicked, the server side will receive two piece of data.
Please insert that both the item and price into database.
Then retrive all data from database,
and display both item and price on web page for all data.

"""
