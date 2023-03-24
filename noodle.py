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

def insert(ID, content, user, time):
      connect = sqlite3.connect('comments.db')
      connect.execute("INSERT INTO COMMENTS (ID,content,user,time) VALUES (?,?,?)", (ID, content, user, time))

@app.route('/join', methods=['GET', 'POST'])
def join():
	if request.method == 'POST':
		firstname = request.form['firstname']
		name = request.form['name']
		email = request.form['email']
		city = request.form['city']
		country = request.form['country']
		phone = request.form['phone']

		with sqlite3.connect("database.db") as users:
			cursor = users.cursor()
			cursor.execute("INSERT INTO PARTICIPANTS (firstname,name,email,city,country,phone) VALUES (?,?,?,?,?,?)", (firstname, name, email, city, country, phone))
			users.commit()
		return render_template("index.html")
	else:
		return render_template('join.html')

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

