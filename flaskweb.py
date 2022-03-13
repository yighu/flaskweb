
#!pip install flask-ngrok
#!pip install flask-bootstrap

from flask_ngrok import run_with_ngrok
from flask import Flask, render_template , request 
import os
from markupsafe import escape
import sqlite3
#from flask_cores import CORS

#Mount the driver
#This is to find the url for flask server host in google colab in case ngrock as login 5000 is the flask port
#from google.colab.output import eval_js
#print(eval_js("google.colab.kernel.proxyPort(5000)"))
# https://z4spb7cvssd-496ff2e9c6d22116-8000-colab.googleusercontent.com/

app = Flask(__name__, template_folder='static')
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
