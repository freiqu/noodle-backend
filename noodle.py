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

def delete(id):
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM COMMENTS WHERE ID=%s" % id)
    connect.commit()

def update(id, new_content):
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    time = str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))[:19]
    cursor.execute("UPDATE COMMENTS SET content = {0}, time = {1} WHERE ID = {2} ;".format(new_content, time, id))
    connect.commit()


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

@app.route('/posts', methods=['DELETE'])
def postsDELETE():
    id = request.json['id']
    delete(id)
    posts = read()
    return Response(posts, status=200, mimetype="application/json")

@app.route('/posts', methods=['PUT'])
def postsPUT():
    id = request.json['id']
    new_content = request.json['new_content']
    update(id, new_content)
    posts = read()
    return Response(posts, status=200, mimetype="application/json")
