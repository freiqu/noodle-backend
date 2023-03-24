from flask import Flask, Response, request, render_template, json
from flask_cors import CORS
import sqlite3
import datetime
import pytz
import secretstorage


current_time = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

app = Flask(__name__)
CORS(app)
user = "Noodle"
curID = 0

connect = sqlite3.connect('comments.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS COMMENTS (ID INTEGER, content TEXT, user TEXT, time TEXT)')


def insert(content, user, time=datetime.datetime.now(pytz.timezone('Europe/Berlin'))):
    global curID
    connect = sqlite3.connect('comments.db')
    connect.execute("INSERT INTO COMMENTS (ID,content,user,time) VALUES (?,?,?,?)",
                    (curID, content, user, time))
    curID += 1


def read():
    connect = sqlite3.connect('comments.db')
    posts = connect.execute('SELECT * FROM COMMENTS;')


@app.route('/')
def index():
    return Response('index.html', status=200, mimetype="text/plain")


@app.route('/news', methods=['GET'])
def news():
    if request.method == 'GET':
        connect = sqlite3.connect('comments.db')
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM COMMENTS')

        data = cursor.fetchall()
        comments = {}
        for i in data:
            pass
        return Response(status=200, mimetype="text/plain")


"""
{
    "posts": {
        "content": "hab heute dies un das gemacht"
        "user": "Reiner Zufall"
        "time": "2023-03-23 14:21:34"
    }
}
"""
