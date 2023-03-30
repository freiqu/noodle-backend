from flask import Flask, Response, request, json
from flask_cors import CORS
import sqlite3
import datetime
import pytz


current_time = datetime.datetime.now(pytz.timezone('Europe/Berlin'))

app = Flask(__name__)
CORS(app)

connect = sqlite3.connect('comments.db')
connect.execute(
    'CREATE TABLE IF NOT EXISTS COMMENTS (ID INTEGER, content TEXT, user TEXT, time TEXT, up INTEGER, down INTEGER)')


def insert(content, user="anonymous"):
    print("Insert:")
    print(content)
    print(user)
    print()
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute("SELECT MAX(ID) FROM COMMENTS")
    id = cursor.fetchall()[0][0]
    if id == None:
        id = 0
    else:
        id = int(id)
        id += 1
    cursor.execute("INSERT INTO COMMENTS (ID,content,user,time,up,down) VALUES (?,?,?,?,?,?)",
                   (id, content, user, str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))[:19], 0, 0))
    connect.commit()
    post = {"id": id, "content": content, "user": user, "time": str(datetime.datetime.now(pytz.timezone('Europe/Berlin')))[:19], "up": 0, "down": 0}
    return json.dumps(post)

def read():
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM COMMENTS')
    data = cursor.fetchall()
    posts = {'comments': []}
    for i in data:
        posts['comments'].append({'id': i[0], 'content': i[1], 'user': i[2], 'time': i[3], "up": i[4], "down": i[5]})
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
    new_content = "\'" + new_content + "\'"
    time = "\'" + time + "\'"
    cursor.execute("UPDATE COMMENTS SET content = {0}, time = {1} WHERE ID = {2} ;".format(new_content, time, id))
    connect.commit()

def thumb(updown, id):
    connect = sqlite3.connect('comments.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM COMMENTS')
    data = cursor.fetchall()
    up = 0
    down = 0
    if id[0] == "d":
        id = int(id[4:])
    elif id[0] == "u":
        id = int(id[2:])
    for i in data:
        if i[0] == id:
            up = i[4]
            down = i[5]
    up += 1
    down += 1
    cursor = connect.cursor()
    if updown == "up":
        print("{} up at {}".format(up, id))
        cursor.execute('UPDATE COMMENTS SET up = {0} WHERE ID = {1};'.format(up, id))
    elif updown == "down":
        print("{} down at {}".format(down, id))
        cursor.execute('UPDATE COMMENTS SET down = {0} WHERE ID = {1};'.format(down, id))
    connect.commit()


@app.route('/posts/thumb', methods=['POST'])
def thumbs():
    updown = request.json['updown']
    id = request.json['id']
    thumb(updown, id)
    posts = read()
    return Response(posts, status=200, mimetype="application/json")

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
