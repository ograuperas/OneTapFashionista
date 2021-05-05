from flask import Flask, send_file, jsonify, request,send_from_directory
from flask_cors import CORS
import json
import os
import cv2
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/coppelia', methods=['GET','POST'])
def hello_world():
    print(request.form['coppeliaid'])
    if request.form['coppeliaid'] == '19999':
        response = jsonify(res="ok")
    else:
        response = jsonify(res="notok")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/getObject.png')
def image():
    return send_file('1.png', mimetype='image/png')

@app.route('/getObject')
def points():

    l = [[10,20],[120,200]]

    return json.dumps(l)

if __name__ == '__main__':
    app.run()
