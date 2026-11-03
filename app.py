from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def weather():
    city = request.args.get('city')

    if not city:
        return render_template('index.html', error="Please enter a city name")

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get('cod') !=200:
        return render_template('index.html', error="City not found")

    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed']
    }

    return render_template('index.html', weather=weather_info)



if __name__ == '__main__':
    app.run(debug=True)