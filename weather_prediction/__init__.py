from flask import Flask,jsonify,request,send_file
from bs4 import BeautifulSoup as soup
import datetime as dt
from datetime import datetime
import requests
import json
from urllib.request import urlopen as req
import pandas as pd
from datetime import datetime,timedelta
import numpy as np



app = Flask(__name__)

@app.route('/get_json_data')
def get_json_data():

    url_f='https://weather.com/en-IN/weather/hourbyhour/l/07d5132b2543887e4d656175575b533c0fe15e1214b4e132d9ae286b18748dcb'
    uclient=req(url_f)
    page_html=uclient.read()
    page_html
    uclient.close()

    page_soup=soup(page_html,'html.parser')
    containers=page_soup.find_all('details',{'class':"DaypartDetails--DayPartDetail--2XOOV DaypartDetails--ctaShown--3JJj3 Disclosure--themeList--1Dz21"})
    sub_containers=containers[0]
    detailed_containers=sub_containers.find_all("div",{'class':"DetailsSummary--DetailsSummary--1DqhO DetailsSummary--hourlyDetailsSummary--2xM-L"})

    extracted_text=[]
    for i in containers:
        sub_containers=i.find_all("div",{'class':"DetailsSummary--DetailsSummary--1DqhO DetailsSummary--hourlyDetailsSummary--2xM-L"})
        time_start=str(sub_containers).find('Name">')+6
        time_end=time_start+5

        sub_containers_condition=i.find_all("div",{'class':"DetailsSummary--condition--2JmHb"})
        time_start_c=str(sub_containers_condition).find('307Ax">')+7
        time_end_c=str(sub_containers_condition).find('</span></div>')

        sub_containers_d=i.find_all("span",{'class':"DetailsSummary--tempValue--jEiXE"})
        time_start_d=str(sub_containers_d).find('"TemperatureValue">')+19
        time_end_d=str(sub_containers_d).find('<span>°')

        extracted_text.append([str(sub_containers)[time_start:time_end],str(sub_containers_condition)[time_start_c:time_end_c],str(sub_containers_d)[time_start_d:time_end_d]])

    print(len(extracted_text))

    data3=pd.DataFrame(extracted_text,columns=['time','condition','temp'])
    #__________________
    containers=page_soup.find_all('div',{'class':"HourlyForecast--DisclosureList--MQWP6"})
    sub_containers=containers[0]
    detailed_containers=sub_containers.find_all("div",{'class':"DaypartDetails--DayPartDetail--2XOOV DaypartDetails--ctaShown--3JJj3 DaypartDetails--enablePreviousBorder--2B1p5 Disclosure--themeList--1Dz21 Disclosure--disableBorder--3Np63"})
    detailed_containers

    extracted_text=[]
    for i in containers:
        sub_containers=i.find_all("div",{'class':"DetailsSummary--DetailsSummary--1DqhO DetailsSummary--hourlyDetailsSummary--2xM-L"})
        time_start=str(sub_containers).find('Name">')+6
        time_end=time_start+5

        sub_containers_condition=i.find_all("div",{'class':"DetailsSummary--condition--2JmHb"})
        time_start_c=str(sub_containers_condition).find('307Ax">')+7
        time_end_c=str(sub_containers_condition).find('</span></div>')

        sub_containers_d=i.find_all("span",{'class':"DetailsSummary--tempValue--jEiXE"})
        time_start_d=str(sub_containers_d).find('"TemperatureValue">')+19
        time_end_d=str(sub_containers_d).find('<span>°')

        extracted_text.append([str(sub_containers)[time_start:time_end],str(sub_containers_condition)[time_start_c:time_end_c],str(sub_containers_d)[time_start_d:time_end_d]])

    print(len(extracted_text))

    data1=pd.DataFrame(extracted_text,columns=['time','condition','temp'])
    #____________________________
    containers=page_soup.find_all('details',{'class':"DaypartDetails--DayPartDetail--2XOOV DaypartDetails--ctaShown--3JJj3 DaypartDetails--enablePreviousBorder--2B1p5 Disclosure--themeList--1Dz21 Disclosure--disableBorder--3Np63"})
    sub_containers=containers[0]
    detailed_containers=sub_containers.find_all("div",{'class':"DaypartDetails--DayPartDetail--2XOOV DaypartDetails--ctaShown--3JJj3 DaypartDetails--enablePreviousBorder--2B1p5 Disclosure--themeList--1Dz21 Disclosure--disableBorder--3Np63"})

    containers
    extracted_text=[]
    for i in containers:
        sub_containers=i.find_all("div",{'class':"DetailsSummary--DetailsSummary--1DqhO DetailsSummary--hourlyDetailsSummary--2xM-L"})
        time_start=str(sub_containers).find('Name">')+6
        time_end=time_start+5

        sub_containers_condition=i.find_all("div",{'class':"DetailsSummary--condition--2JmHb"})
        time_start_c=str(sub_containers_condition).find('307Ax">')+7
        time_end_c=str(sub_containers_condition).find('</span></div>')

        sub_containers_d=i.find_all("span",{'class':"DetailsSummary--tempValue--jEiXE"})
        time_start_d=str(sub_containers_d).find('"TemperatureValue">')+19
        time_end_d=str(sub_containers_d).find('<span>°')

        extracted_text.append([str(sub_containers)[time_start:time_end],str(sub_containers_condition)[time_start_c:time_end_c],str(sub_containers_d)[time_start_d:time_end_d]])

    print(len(extracted_text))

    data2=pd.DataFrame(extracted_text,columns=['time','condition','temp']).head(1)
    weather_data=pd.concat([data1,data2,data3],axis=0)
    weather_data.to_csv('../weatherdata.csv')
    list_of_dicts = weather_data.to_dict(orient='records')

    return jsonify({"data": list_of_dicts})



if __name__ == '__main__':
    app.run(debug=True) 
