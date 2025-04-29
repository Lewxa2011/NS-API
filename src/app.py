from flask import Flask
import threading
import requests
import time

app = Flask(__name__)

heartbeat_started = False

def send_heartbeat():
    while True:
        try:
            requests.get("https://ns-api-970c.onrender.com/")
            print("Heartbeat sent")
        except requests.exceptions.RequestException as e:
            print(f"Error sending heartbeat: {e}")
        time.sleep(10)

@app.before_request
def start_heartbeat():
    global heartbeat_started
    if not heartbeat_started:
        heartbeat_started = True
        heartbeat_thread = threading.Thread(target=send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)