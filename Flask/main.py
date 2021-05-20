from flask import Flask, send_file, jsonify, request,send_from_directory
from flask_cors import CORS
import json

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
@app.route('/getImage', methods=['GET','POST'])
def hello_world():

    content = request.get_json()
    resposta = content['image']
    print(resposta)

    response = jsonify(res="ok")

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response






if __name__ == '__main__':
    app.run()
