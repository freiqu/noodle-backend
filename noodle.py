from flask import Flask, Response, request, json
from flask_cors import CORS
import sqlite3
import datetime
import pytz


current_time = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

app = Flask(__name__)
CORS(app)
user = "Noodle"

connect = sqlite3.connect('comments.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS COMMENTS (ID INTEGER, content TEXT, user TEXT, time TEXT)')


def insert(content, user="anonymous"):
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute("SELECT MAX(ID) FROM COMMENTS")
    id = cursor.fetchall()[0][0]
    if id == None:
        id = 0
    else:
        id = int(id)
        id += 1
    cursor.execute("INSERT INTO COMMENTS (ID,content,user,time) VALUES (?,?,?,?)",
                   (id, content, user, str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))[:19]))
    connect.commit()
    post = {"id": id, "content": content, "user": user, "time": str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))[:19]}
    return json.dumps(post)


def read():
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM COMMENTS')
    data = cursor.fetchall()
    posts = {'comments': []}
    for i in data:
        posts['comments'].append(
            {'id': i[0], 'content': i[1], 'user': i[2], 'time': i[3]})
    comments = json.dumps(posts)
    return comments


@app.route('/')
def index():
    return Response('index.html', status=200, mimetype="text/plain")

@app.route('/posts', methods=['GET'])
def postsGET():
    posts = read()
    return Response(posts, status=200, mimetype="application/json")

@app.route('/posts', methods=['POST'])
def postsPOST():
    user = request.json["user"]
    content = request.json["content"]
    post = insert(content, user)
    return Response(post, status=200, mimetype="application/json")


"""
{
    "posts": {
        "content": "hab heute dies und das gemacht"
        "user": "Reiner Zufall"
        "time": "2023-03-23 14:21:34"
    }
}
"""
