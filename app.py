from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
AI_KEY = os.getenv('AI_KEY')

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
        'wind': data['wind']['speed'],
        'condition': data['weather'][0]['main'].lower()
    }

    ai_suggestion = get_ai_suggestion(weather_info)
    return render_template('index.html', weather=weather_info, ai_suggestion=ai_suggestion)

def get_ai_suggestion(weather):
    prompt = (
        f"The current weather in {weather['city']} is {weather['description']} "
        f"with temperature {weather['temperature']}°C. "
        "Give a short and friendly suggestion for what to wear or do today."
    )

    try:
        ai_response = requests.post(
            "https://ai.hackclub.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {AI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100
            },
            timeout=10
        )
        result = ai_response.json()
        suggestion = result['choices'][0]['message']['content']
        return suggestion
    except Exception:
        return "AI suggestion is not available right now."

if __name__ == '__main__':
    app.run(debug=True)