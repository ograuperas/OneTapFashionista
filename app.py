from flask import Flask, send_file, jsonify
from flask_cors import CORS
import cv2
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/a', methods=['GET','POST'])
def hello_world():
    response = jsonify(title="hello world")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/f')
def image():
    """
    image = cv2.imread('1.png')
    cv2.imshow('image', image)



    return {
        "image": image.tolist()
    }
    """
    return send_file('1.png', mimetype='image/gif')

if __name__ == '__main__':
    app.run()
