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
import utils

app = Flask(__name__)
CORS(app)
LABELS_utils = ['Background', 'Hat', 'Hair', 'Glove', 'Sunglasses', 'Upper-clothes', 'Dress', 'Coat',
                    'Socks', 'Pants', 'Jumpsuits', 'Scarf', 'Skirt', 'Face', 'Left-arm', 'Right-arm', 'Left-leg',
                    'Right-leg', 'Left-shoe', 'Right-shoe']

@app.route('/getImage', methods=['GET', 'POST'])
def getImage():
    global LABELS_utils
    content = request.get_json()
    resposta = content['image']

    image = bytes(resposta)
    nparr = np.frombuffer(image, np.uint8)
    im_input = cv2.imdecode(nparr, 1)

    #TODO MODEL RETURN OUTPUT

    im_output = cv2.imread('O:/Escriptori/SM/Flask/img/out/out.png')


    colors = utils.get_palette(20)
    labels_in_image = utils.return_labels(im_output, LABELS_utils, colors)

    iconMap = {'Hat': 10, 'Upper-clothes': 8, 'Dress': 2, 'Coat': 9,'Socks': 6, 'Pants': 1, 'Jumpsuits': 7, 'Scarf': 3, 'Skirt': 5}
    llista = []
    for i in labels_in_image:
        llista.append({'icon': iconMap[i], 'name': i})

    aux = {'llista': llista, 'res': 'ok'}

    response = jsonify(aux)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/returnImage', methods=['GET', 'POST'])
def returnImage():
    content = request.get_json()
    resposta = content
    print(resposta)

    im_input = cv2.imread('O:/Escriptori/SM/Flask/img/in/in.jpg') #input Model
    im_output = cv2.imread('O:/Escriptori/SM/Flask/img/out/out.png') #Output Model

    colors = utils.get_palette(20)
    global LABELS_utils

    iconMap = {10: 'Hat', 8: 'Upper-clothes', 2: 'Dress', 9: 'Coat', 6: 'Socks', 1: 'Pants', 7: 'Jumpsuits', 3: 'Scarf', 5: 'Skirt'}
    textureMap = {0: 'O:/Escriptori/SM/Flask/patterns/blue_feathers.jpg',
                  1: 'O:/Escriptori/SM/Flask/patterns/blue_feathers.jpg',
                  2: 'O:/Escriptori/SM/Flask/patterns/heads.jpg',
                  3: 'O:/Escriptori/SM/Flask/patterns/olivo.jpg'}

    LABELS_K_VOLS = iconMap[resposta['roba']]

    cloth_in_image, mask = utils.is_label_in_image(im_output, LABELS_K_VOLS, LABELS_utils, colors)
    mask_uint8 = mask.astype('uint8') * 255

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

    success, encoded_image = cv2.imencode('.png', im_input)
    content2 = np.concatenate(encoded_image, axis=0)

    response = jsonify(imatge=content2.tolist())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"  # keep alive
    app.run()
#python3 simple_extractor.py --dataset 'lip' --model-restore 'checkpoints/final.pth' --input-dir 'inputs' --output-dir 'outputs'