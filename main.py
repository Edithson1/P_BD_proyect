from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask with SQLAlchemy!'

