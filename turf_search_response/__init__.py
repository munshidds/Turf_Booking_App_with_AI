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

@app.route('/turf_search_response',methods=['POST','GET'])
def search_response():

    try:
        data = request.get_json()  
        print(data,'from search_response________________________________________________________________')
        
        user_input = data[0]['name']
        print(user_input)

        api_url_search = 'http://13.126.57.93:8000/owner/turf-display-all/'
        search_rquest_turf = requests.get(api_url_search)
        if search_rquest_turf.status_code == 200:
            data = search_rquest_turf.json()
            print(data)
            data=pd.DataFrame(data)
            print(data)
            data.to_csv('../turf_details.csv')  
        # user_input = "Golden Turf Gardens"
        df=pd.read_csv('../turf_details.csv')
        matches = process.extract(user_input,list(df.name) )
        print(matches)

        threshold = 60

        similar_turfs = [match for match in matches if match[1] >= threshold]
        list_=[]
        if similar_turfs:
            print("Similar Turfs:")
            for turf, confidence in similar_turfs:
                df[df['name']==turf]
                list_.append(turf)
            
            list_2 = []

            for name in list_:
                matching_rows = df[df['name'].str.strip().str.lower() == name.strip().lower()]
                # print(matching_rows,"_________________________________________________")

                if not matching_rows.empty:
                    list_2.append(matching_rows.to_dict(orient='records')[0])

            return list_2
        else:
            return "No similar turfs found."
    except:
        return "No similar turfs found"

if __name__ == '__main__':
    app.run(debug=True) 

