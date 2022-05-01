#https://replit.com/talk/learn/Flask-Tutorial-Part-1-the-basics/26272
#to get it work in replit
#!pip install flask-ngrok
#!pip install flask-bootstrap
import random, string
#from flask_ngrok import run_with_ngrok
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
#run_with_ngrok(app)

def setupDb():
    conn = sqlite3.connect('test.db')
    print("Opened database successfully");

    conn.execute('''
CREATE TABLE IF NOT EXISTS attendance(classname text, teacher text, student text, date text, attended text);      
                 ''')
    conn.execute('''
CREATE TABLE IF NOT EXISTS classname(name text, teacher text);                 
                 ''')
    conn.execute('''
CREATE TABLE IF NOT EXISTS student(name text, email text);                 
                 ''')
  
    conn.commit()

    print("Table created successfully");

    conn.close()

def insertClass(classname, teacher):
  conn = sqlite3.connect('test.db')
  conn.execute(f"INSERT INTO classname VALUES('{classname}', '{teacher}');")
  conn.commit()
  conn.close()
  
def insertStudent(name, email):
  conn = sqlite3.connect('test.db')
  conn.execute(f"INSERT INTO student VALUES('{name}', '{email}');")
  conn.commit()
  conn.close()  
def readClass():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM classname''')
  result=' results <br>'
  for row in cursor:
    #print(row)
    result = result +"<br>" +row[0]
  
  conn.close()
  return result
def getClassDataArray():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM classname''')
  data = cursor.fetchall()
  conn.close()
  return data  

def insert(classname, teacher, student, date, attended):
  print(f'to insert {classname}')
  conn = sqlite3.connect('test.db')
  conn.execute(f"INSERT INTO attendance VALUES('{classname}', '{teacher}','{student}','{date}','{attended}');")
  conn.commit()
  print("data inserted successfully");
  conn.close()

def getData():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM attendance''')
  result=' results <br>'
  for row in cursor:
    #print(row)
    result = result +"<br>" +row[0]
  
  conn.close()
  return result


def getDataArray():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM attendance''')
  data = cursor.fetchall()
  conn.close()
  return data

@app.route('/')
def hello():
  return 'hello world!'



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



@app.route('/attendance', methods=['GET','POST'])
def recordattendance():
    if request.method=='GET':
      pass
    classdata = getClassDataArray()
    data = getDataArray()  
    return render_template('attendance_v2.html', items = data, classes = classdata)


@app.route('/class', methods=['GET','POST'])
def displayclass():
    if request.method=='GET':
      pass
   
    data = getClassDataArray()  
    return render_template('classname.html', items = data)

@app.route('/student', methods=['GET','POST'])
def displaystudent():
    if request.method=='GET':
      pass
   
    data = getStudentDataArray()  
    return render_template('student.html', items = data)



@app.route('/mp', methods=['GET', 'POST'])
def map():
    if request.method=='GET':
      pass
    if request.method=='POST':
      classname=request.form.get('classname')
      teacher=request.form.get('teacher')
      student=request.form.get('student')
      date=request.form.get('date')
      attended=request.form.get('attended')


      insert(classname, teacher, student, date, attended )
    items=getDataArray()
    return render_template('attendance.html', items=items)

@app.route('/saveclass', methods=['GET', 'POST'])
def mapclass():
    if request.method=='GET':
      pass
    if request.method=='POST':
      classname=request.form.get('classname')
      teacher=request.form.get('teacher')

      insertClass(classname, teacher)
    items=getClassDataArray()
    return render_template('classname.html', items=items)

#From coding perspective (steps to develop a working web page):
#1. create a new table
#2. add method to insert data to table
  
#3. add method to read data (as string) and as array (Chuling)
#4. create html page (template) (David)
#5. add method to bring up the html page (Joseph)
#6. add a method to do transaction (Austin)

@app.route('/savestudent', methods=['GET', 'POST'])
def mapstudent():
    if request.method=='GET':
      pass
    if request.method=='POST':
      studentname=request.form.get('name')
      email=request.form.get('email')

      insertStudent(studentname, email)
    items=getStudentDataArray()
    return render_template('student.html', items=items)








def getStudentDataArray():
  conn = sqlite3.connect('test.db')
  cursor = conn.execute(''' SELECT *  FROM student''')
  data = cursor.fetchall()
  conn.close()
  return data  


if __name__ == '__main__':
   setupDb()
   app.run(host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
                port=random.randint(2000, 9000))