from flask import Flask, jsonify

if(__name__ == "__main__"):
    app = Flask(__name__)
    app.run('0.0.0.0', 443, False)