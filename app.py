import threading
from flask import Flask
import bot

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<p>sup</p>"

@app.route("/ping", methods=["GET"])
def ping():
    return ""

@app.route("/start", methods=["GET"])
def start():
    bot.start()
    return "<p>Bot initiated.</p>"