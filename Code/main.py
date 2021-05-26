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
from google.cloud import storage
from datetime import datetime

import utils

app = Flask(__name__)
CORS(app)
LABELS_utils = ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat',
                    'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm', 'Left-leg',
                    'Right-leg', 'Left-shoe', 'Right-shoe']
input_image = ''
output_image = ''

@app.route('/getImage', methods=['GET', 'POST'])
def getImage():
    global LABELS_utils
    global input_image
    global output_image

    content = request.get_json()
    resposta = content['image']

    #Descodifiquem l'imatge, aquesta és rebuda com una llista de bytes i la convertim a numpy array
    image = bytes(resposta)
    nparr = np.frombuffer(image, np.uint8)
    im_input = cv2.imdecode(nparr, 1)
    
    im_output, input_image, output_image = utils.return_mask(im_input)

    im_output = cv2.imread('/workspace/img/out/' + output_image) 
    
    #Cridem a la funcio que ens retorna una llista amb els elements de roba detectats a l'imatge
    colors = utils.get_palette(20)
    labels_in_image = utils.return_labels(im_output, LABELS_utils, colors)

    #Map dels elements que detecta el model per poder passar els identificadors a l'app
    iconMap = {'Hat': 10, 'Upper-clothes': 8, 'Dress': 2, 'Coat': 9,'Socks': 6, 'Pants': 1, 'Jumpsuits': 7, 'Scarf': 3, 'Skirt': 5}
    llista = []
    for i in labels_in_image:
        llista.append({'icon': iconMap[i], 'name': i})

    aux = {'llista': llista, 'res': 'ok'}

    #Enviem com a resposta un JSON amb les caracteristiques de la imatge
    response = jsonify(aux)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/returnImage', methods=['GET', 'POST'])
def returnImage():
    global input_image
    global output_image
    content = request.get_json()
    resposta = content
    print(resposta)

    im_input = cv2.imread('/workspace/img/in/' + input_image) #input Model
    im_output = cv2.imread('/workspace/img/out/' + output_image) #Output Model

    colors = utils.get_palette(20)
    global LABELS_utils

    #Map per convertir els elements seleccionats per l'usuari a l'app a el que enten el codi back-end
    iconMap = {10: 'Hat', 8: 'Upper-clothes', 2: 'Dress', 9: 'Coat', 6: 'Socks', 1: 'Pants', 7: 'Jumpsuits', 3: 'Scarf', 5: 'Skirt'}
    textureMap = {0: '/workspace/patterns/blue_feathers.jpg',
                  1: '/workspace/patterns/heads.jpg',
                  2: '/workspace/patterns/olivo.jpg'}
    
    LABELS_K_VOLS = iconMap[resposta['roba']]
    
    cloth_in_image, mask = utils.is_label_in_image(im_output, LABELS_K_VOLS, LABELS_utils, colors)
    mask_uint8 = mask.astype('uint8') * 255

    #Depenent si l'usuari ha escollit canviar el color o posar una textura es cridarà a la funció corresponent
    if resposta['isColor']:
        hex = resposta['color']
        hex = hex.lstrip('#')
        hlen = len(hex)
        rgbs = list(tuple(int(hex[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3)))
        rgb = np.flip(np.asarray(rgbs))
        im_input = utils.change_colour(im_input, mask_uint8, rgb)
    else:
        pattern = cv2.imread(textureMap[resposta['textura']])
        im_input = utils.change_pattern(im_input, mask_uint8, pattern)
    
    #obtenim la data i l'hora actual per identificar les imatges de manera unica
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    
    #realitzem la connexió amb Cloud Storage
    client = storage.Client()
    bucket = client.get_bucket('onetapfashionista.appspot.com')
    blob = bucket.blob('img_'+dt_string +'.png')
    
    #Codifiquem l'imatge a llista de bytes per tal que el client la pugui interpretar.
    success, encoded_image = cv2.imencode('.png', im_input)
    content2 = np.concatenate(encoded_image, axis=0)
    
    #guardem la imatge generada a Cloud Storage
    blob.upload_from_string(bytes(content2), content_type='image/png')
    
    #Enviem com a resposta un JSON amb l'imatge codificada
    response = jsonify(imatge=content2.tolist())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"  #s'utilitza per poder tenir una connexió de tipus Keep-Alive
    app.run()

