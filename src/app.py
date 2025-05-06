from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cool')
def cool():
    return render_template('cool.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required.'}), 400

    # Use wttr.in for no-key weather
    url = f"https://wttr.in/{city}?format=j1"
    resp = requests.get(url)
    if resp.status_code != 200:
        return jsonify({'error': 'City not found or API error.'}), resp.status_code

    data = resp.json()
    # Extract relevant info
    current = data['current_condition'][0]
    weather = {
        'name': city.title(),
        'temp': current['temp_C'],
        'feels_like': current['FeelsLikeC'],
        'humidity': current['humidity'],
        'wind': current['windspeedKmph'],
        'description': current['weatherDesc'][0]['value']
    }
    return jsonify(weather)

if __name__ == '__main__':
    app.run(debug=True)