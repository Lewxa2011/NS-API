import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required.'}), 400

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({'error': 'City not found or API error.'}), resp.status_code

    data = resp.json()
    weather = {
        'name': data['name'],
        'country': data['sys']['country'],
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed'],
        'description': data['weather'][0]['description']
    }
    return jsonify(weather)

if __name__ == '__main__':
    app.run(debug=True)