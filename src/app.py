from flask import Flask
import threading
import requests
import time

app = Flask(__name__)

# Function to send a heartbeat request every 10 seconds
def send_heartbeat():
    while True:
        try:
            requests.get("https://ns-api-970c.onrender.com/")
            print("Heartbeat sent")
        except requests.exceptions.RequestException as e:
            print(f"Error sending heartbeat: {e}")
        time.sleep(10)

# Start the heartbeat thread when the app receives its first request
@app.before_first_request
def start_heartbeat():
    # Start the heartbeat in a separate thread
    heartbeat_thread = threading.Thread(target=send_heartbeat)
    heartbeat_thread.daemon = True  # Allows the thread to exit when the app exits
    heartbeat_thread.start()

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)