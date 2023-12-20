from flask import Flask,jsonify,request,send_file
import requests


app = Flask(__name__)


@app.route('/current_weather', methods=['POST'])
def weather():

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = '1f5da08cb47d3cc87ac91f78a97f435a'
    CITY = 'calicut'
    url =BASE_URL + "appid=" + "1f5da08cb47d3cc87ac91f78a97f435a" + "&q=" +  CITY
    response =requests.get(url).json()
    temperature_kelvin = response['main']['temp']
    temperature_celsius = temperature_kelvin - 273.15

    return jsonify({"data":10})






if __name__ == '__main__':
    app.run(debug=True) 
