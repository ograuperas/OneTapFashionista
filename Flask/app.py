import cv2
from flask import Flask, send_file, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import io
import os
import PIL.Image as Image
import numpy as np
import matplotlib.pyplot as plt
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
CORS(app)
"""
#EXEMPLE FUNCIONA
@app.route('/coppelia', methods=['GET','POST'])
def hello_world():

    content = request.get_json()
    resposta = content['coppeliaid']

    if resposta == '19999':
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

-> possibles endpoints: 
     1) rebre una imatge,
        identificar peçes de roba -> si 0 error
        guardar imatge a bd

    2)  rebre id imatge bd i color
        canviar color
        retornar imatge



"""

@app.route('/getImage', methods=['GET', 'POST'])
def getImage():
    content = request.get_json()
    resposta = content['image']

    image = bytes(resposta)#Image.open(io.BytesIO(bytes(resposta)))
    #cv2.imshow("disp", image)

    nparr = np.frombuffer(image, np.uint8)
    img_np = cv2.imdecode(nparr, 1)
    plt.imshow(img_np)
    plt.show()
    #print(resposta)
    response = jsonify(res="ok")

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/returnImage', methods=['GET', 'POST'])
def returnImage():
    image = cv2.imread('O:/Escriptori/SM/Flask/3.PNG')
    success, encoded_image = cv2.imencode('.png', image)
    content2 = np.concatenate(encoded_image, axis=0)
    #content1 == content2
    image = bytes(content2.tolist())  # Image.open(io.BytesIO(bytes(resposta)))
    # cv2.imshow("disp", image)

    nparr = np.frombuffer(image, np.uint8)
    img_np = cv2.imdecode(nparr, 1)
    plt.imshow(img_np)
    plt.show()
    response = jsonify(imatge=content2.tolist())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

    #return send_file('O:/Escriptori/SM/Flask/3.PNG', mimetype='image/png')

@app.route('/llistaRoba')
def points():

    l = ['trousers', 'shoes', 'hat']

    return json.dumps(l)

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1" #keep alive
    app.run()
