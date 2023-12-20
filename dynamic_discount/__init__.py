 
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

@app.route('/dynamic_discount',methods=['POST','GET'])
def dynamic_discount():
    try:
        data = request.get_json()
        print(data)

        start_time = data['date'] + " " + data['start_time']
        end_time   = data['date'] + " " + data['end_time']
        print(start_time)
        print(end_time)

        predict_data=[]

        date_string=data['date']        #____________________________________________________________________
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        day_format = date_object.strftime('%A')
        if day_format == 'Sunday' or 'Saturday':
            predict_data.append(0)
        elif day_format == 'Friday':
            predict_data.append(1)
        else:
            predict_data.append(2)

        time_string = data['start_time']      #_______________________________________________________________________
        input_time = datetime.strptime(time_string, '%H:%M:%S').time()
        print('input_time',input_time)

        if input_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
            predict_data.append(1)
        elif input_time < datetime.strptime('16:00:00', '%H:%M:%S').time():
            predict_data.append(2)
        else:
            predict_data.append(0)
        
        #   customer level
        try:
            play_ratio=data['booking_count']/90
            if play_ratio <=.05:
                predict_data.append(0)
            if play_ratio < .35:
                predict_data.append(1)
            if play_ratio >= .35:
                predict_data.append(2)
            print('play_ratio',play_ratio)
        except:
            predict_data.append(1)

        df=pd.read_csv('../weatherdata.csv')
        input_time = datetime.strptime(time_string, '%H:%M:%S').time()
        half_hour = timedelta(minutes=30)
        new_time = (datetime.combine(datetime.min, input_time) + half_hour).time()
        new_time=str(new_time)
        time=new_time[:5]
        temperature=list(df[df['time']==time]['temp'])[0]
        predict_data.append(temperature)

        try:
            turf_rating = data['turf_rating'] #____________________________________________________________________________
            predict_data.append(turf_rating)
        except:
            predict_data.append(4)

        weather_conditions=['T-Storms','Scattered T-Storms']
        weather_c='Scattered T-Storms'   #___________________________________________________
        if weather_c in weather_conditions:
            predict_data.append(1)    
        else:
            predict_data.append(0)

        print('predict_data',predict_data)
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, '../dynamic_discound_model')
            model = joblib.load(model_path)

        except:
            print('error from model predition')
        result =model.predict([predict_data])  * data['price']

        data['discount_amount']=int(result[0])

        return jsonify({"data": data})
    except:
        return jsonify({"data":{
    "booking_count": np.nan,
    "date": np.nan,
    "discount_amount":np.nan,
    "end_time": np.nan,
    "price": np.nan,
    "start_time": np.nan,
    "turf": np.nan,
    "user":np.nan}})

if __name__ == '__main__':
    app.run(debug=True) 
