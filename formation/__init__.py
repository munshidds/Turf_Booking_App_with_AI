from flask import Flask,jsonify,request,send_file
import datetime as dt
from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as req
import pandas as pd
from datetime import datetime,timedelta
from fuzzywuzzy import process
import numpy as np
import cv2
import numpy as np
import joblib
import sklearn
import os
import tempfile


app = Flask(__name__)


@app.route('/formation_img', methods=['POST', 'GET'])
def formation_img():
    try:
        if request.method == 'POST':
            image_file = request.files['image']
            image_array = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)            
            print(img,'__________________________________________________')

            if img is not None:
                haar_cascade = cv2.CascadeClassifier('../haarcascade_mcs_upperbody.xml')
                image = cv2.resize(img, (800, 800))
                
                try:
                    faces = haar_cascade.detectMultiScale(image, 1.1, 9)
                    if len(faces) == 1:
                        x, y, width, height = faces[0]
                        cropped_image = image[y-30:y + height+60, x-30:x + width+30]
                        temp_filename = tempfile.mktemp(suffix='.jpg')
                        cv2.imwrite(temp_filename, cropped_image)

                        return send_file(temp_filename, as_attachment=True, download_name='cropped_image.jpg')
                    
                    elif len(faces) >= 2:
                        temp_filename = tempfile.mktemp(suffix='.jpg')
                        cv2.imwrite(temp_filename, image)

                        return send_file(temp_filename, as_attachment=True, download_name='image.jpg')                    
                    else:
                        temp_filename = tempfile.mktemp(suffix='.jpg')
                        cv2.imwrite(temp_filename, image)

                        return send_file(temp_filename, as_attachment=True, download_name='image.jpg')                
                except:
                    image = cv2.imread(r'../static/images/face 13.png')
                    temp_filename = tempfile.mktemp(suffix='.jpg')
                    cv2.imwrite(temp_filename, image)

                    return send_file(temp_filename, as_attachment=True, download_name='image.jpg')            
            else:
                image = cv2.imread(r'../static/images/face 13.png')
                temp_filename = tempfile.mktemp(suffix='.jpg')
                cv2.imwrite(temp_filename, image)

                return send_file(temp_filename, as_attachment=True, download_name='cropped_image.jpg')
    except:
        image = cv2.imread(r'../static/images/face 13.png')
        temp_filename = tempfile.mktemp(suffix='.png')
        cv2.imwrite(temp_filename, image)

        return send_file(temp_filename, as_attachment=True, download_name='cropped_image.png')


if __name__ == '__main__':
    app.run(debug=True) 


