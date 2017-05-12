import os
import sqlite3
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
sys.path.append('../')

import glob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    text = request.form['text']
    if text=='':
        return render_template('index.html')
    else:
        if os.path.exists("templates/temp/"):
            for CleanUp in glob.glob("templates/temp/*.*"):
                os.remove(CleanUp)
        else:
            os.makedirs("templates/temp/")                           
        qname = text.replace(' ','_')
#	with open('templates/answer.html', 'r+') as f:
#	    f.seek(0)
#	    f.write(demo.get_answer(text, '90e7acx197-nlc-170').encode('utf-8'))
#	    f.truncate()
        with open('templates/temp/'+qname+'.html', 'w+') as f:
            f.seek(0)
            f.write('<h4>The text you entered is: </h4><br/><div style="width:100%;height:500px;line-height:3em;overflow:scroll;padding:5px;background-color:#FFFFFF;color:#B0A2AA;scrollbar-base-color:#EFEFEF;">')
            f.write('<p>' + text + '</p>')
            f.write('</div>')
            
            f.truncate()
        return render_template('index.html', answer='temp/'+qname+'.html', text = 'tmp')


if __name__ == "__main__":
    extra_files = ['templates/answer.html',]
    app.run(extra_files=extra_files)
