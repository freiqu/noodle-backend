from flask import Flask, Response, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['GET'])
def getScore():
    
    return Response("Hello, World", status=200, mimetype="text/plain")