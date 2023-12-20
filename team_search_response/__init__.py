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

@app.route('/team_search_response',methods=['POST','GET'])
def team_search_response():       
    
    try:
        data = request.get_json()  
        print(data,'from search_response________________________________________________________________')
        
        user_input = data[0]['name']
        print(user_input)

        api_url_team_search = 'http://192.168.1.21:9000/user/player/'
        search_request_team = requests.get(api_url_team_search)
        if search_request_team.status_code == 200:
            data = search_request_team.json()
            data=pd.DataFrame(data)
            # data.to_csv('../team_details.csv')

        # user_input = "munshid"
        df=pd.read_csv('../team_details.csv')
        print(df)
        matches = process.extract(user_input,list(df.team_name) )
        print(matches)

        threshold = 70
        similar_name = [match for match in matches if match[1] >= threshold]
        list_=[]
        if similar_name:
            print("similar_name:")
            for team, confidence in similar_name:
                df[df['team_name']==team]
                list_.append(team)        
            list_2 = []
            for name in list_:
                matching_rows = df[df['team_name'].str.strip().str.lower() == team.strip().lower()]
                if not matching_rows.empty:
                    list_2.append(matching_rows.to_dict(orient='records')[0])

            return list_2
        else:
            return "No similar team found."
    except:
        return "No similar team found"
if __name__ == '__main__':
    app.run(debug=True) 

 
