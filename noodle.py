from flask import Flask, Response, request, render_template
from flask_cors import CORS
import sqlite3
import datetime
import pytz

current_time = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

app = Flask(__name__)
CORS(app)

connect = sqlite3.connect('comments.db')
connect.execute(
	'CREATE TABLE IF NOT EXISTS COMMENTS (ID INTEGER, content TEXT, user TEXT, time TEXT)')

def insert():
      connect = sqlite3.connect('comments.db')
      connect.execute('''INSERT INTO COMMENTS ()
      ''')

@app.route('/hello', methods=['GET'])
def getScore():
    return Response("Hello, World", status=200, mimetype="text/plain")

@app.route('/news')
def participants():
	connect = sqlite3.connect('comments.db')
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM COMMENTS')
	data = cursor.fetchall()
	return render_template("news.html", data=data)