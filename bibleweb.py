import random, string
#from flask_ngrok import run_with_ngrok
from flask import Flask, render_template , request 
import os
from markupsafe import escape
from biblemodule import Bible
#from flask_cores import CORS

app = Flask(__name__, template_folder='static')
#CORS(app)
#run_with_ngrok(app)
kjv_url = "https://raw.githubusercontent.com/yighu/python/main/files/kjv.txt"
bible = Bible(kjv_url)  
@app.route('/', methods=['GET', 'POST'])
def mapstudent():
    key = ""
    if request.method=='GET':
      pass
    if request.method=='POST':
      key=request.form.get('key')
    theverses = bible.findVerseContains(key)  
    return render_template('bible.html', items = theverses)

if __name__ == '__main__':
   app.run(host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
                port=random.randint(2000, 9000))